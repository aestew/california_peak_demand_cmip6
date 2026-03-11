# ClimateFEAT: Climate-Informed Forecasting of Electricity with Attention-Based Transformers

## Architecture Overview

ClimateFEAT is a multi-stream transformer model that predicts per-capita electricity demand across California's 58 counties using downscaled CMIP6 climate projections. The model uses five parallel attention streams with cross-attention fusion, each processing a distinct feature group through its own self-attention layers before combining them.

## Target Variable

The model predicts log per-capita maximum daily electricity usage: max_elec_per_capita_log = log(max_daily_electricity / total_pop). Predictions are converted back to MWh by exponentiating and multiplying by county population. This log-per-capita formulation normalizes across counties of vastly different sizes and stabilizes training.

---

## The Five Input Streams and Their Feature Selections

Each stream has its own StandardScaler and processes a specific feature group. Every stream except Geo receives a prepended county embedding token via a learned embedding (58 counties, 8-dimensional embedding).

### Stream 1 — Weather + Time (15 features → 16 tokens with county)

tmax_k_pop, tmin_k_pop, trange_k, cdd65_pop, hdd65_pop, cdd75_pop, spfh_peak_kgkg_pop, wind_peak_ms_pop, dpd_k, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017.

This stream captures same-day thermodynamic drivers and their interaction with temporal demand patterns. Embed dim: 32, 8 attention heads, 2 attention blocks.

### Stream 2 — Rolling Temporal (11 features → 12 tokens with county)

cdd65_pop_roll5, hdd65_pop_roll5, tmax_k_pop_roll5_max, tmax_k_pop_roll7_mean, dpd_k_roll5, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017.

Captures sustained thermal stress via 5-day and 7-day rolling aggregates. The overlap of temporal and baseline features with Stream 1 is intentional — each stream learns different interactions through its own attention weights. Embed dim: 32, 8 heads, 2 attention blocks.

### Stream 3 — Geographic/Structural (4 numeric features + county embedding)

total_pop, per_cap_income, baseline_mw_per_capita_2017, baseline_mw_monthly_2017.

Unlike other streams, this uses a dense feedforward network (Linear → ReLU → Dropout) rather than attention, since it has only 4 slow-moving structural features. County embedding is concatenated directly with the numeric features. Output dim: 32.

### Stream 4 — Heat Wave (5 features → 6 tokens with county)

baseline_mw_per_capita_2017, per_cap_income, cdd75_pop, dpd_k_roll5, cdd65_pop.

A dedicated stream for extreme heat events, using a deliberately larger embedding dimension (64 vs 32 for other streams) to give the model more capacity for high-impact tail events. This stream focuses on the intersection of severe cooling demand (CDD75), humidity stress (dew point depression), and county-level economic and structural characteristics. Embed dim: 64, 8 heads, 2 attention blocks.

### Stream 5 — Infrastructure + Time (11 features → 12 tokens with county)

cuml_count, cuml_sq_foot, cuml_utility_cap, cuml_dc_load, bev, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017.

Captures structural demand growth from data centers and EV adoption, crossed with temporal features to learn seasonality of electrification load. Embed dim: 32, 8 heads, 2 attention blocks.

---

## Cross-Attention Fusion

Streams 1 through 4 (Weather, Rolling, Geo, Heat Wave) are each projected to a shared cross-attention dimension of 64 via learned linear projections, producing 4 tokens. These 4 tokens pass through a single cross-attention block (64-dim, 8 heads), allowing the model to learn how weather interacts with geography, how rolling conditions modify heat wave impact, etc. The output is flattened to 256 dimensions (4 tokens × 64 dims).

Stream 5 (Infrastructure) bypasses cross-attention entirely — its flattened output is concatenated directly with the cross-attention output before the prediction head. This design choice reflects the hypothesis that infrastructure growth is relatively independent of weather-climate interactions and acts more as an additive structural shift.

---

## Prediction Head

The concatenated vector (cross-attention output + infrastructure stream) passes through a 3-layer feedforward head: Linear(→256) → ReLU → Dropout(0.2) → Linear(→64) → ReLU → Dropout(0.1) → Linear(→1).

---

## Engineered Features

**Dew point depression (dpd_k):** Derived from specific humidity (spfh_peak_kgkg_pop) via conversion to vapor pressure, then to dew point temperature, then subtracted from tmax_k_pop. Large values indicate dry conditions, small values indicate high humidity and thermal discomfort. Clipped at zero.

**Rolling aggregates:** cdd65_pop_roll5 (5-day sum of CDD65), hdd65_pop_roll5 (5-day sum of HDD65), tmax_k_pop_roll5_max (5-day max of daily max temperature), tmax_k_pop_roll7_mean (7-day mean of daily max temperature), dpd_k_roll5 (5-day mean dew point depression).

**2017 baselines:** baseline_mw_per_capita_2017 (annual county-level per-capita demand from 2017) and baseline_mw_monthly_2017 (monthly variant). These anchor every stream to a county's structural consumption profile.

**Per capita income:** Imputed using county median, falling back to global median where missing. Adjusted for inflation (per_cap_income).

---

## Data Split

Train: 2018–2021. Validation: 2022. Test: 2023. No temporal leakage — all rolling features computed within each split. Day of week encoded via integer mapping from string labels.

---

## Training Configuration

Optimizer: AdamW, learning rate 3e-4, weight decay 1e-3. Loss: MSE on log per-capita target. Scheduler: ReduceLROnPlateau, patience 5, factor 0.5. Gradient clipping: max norm 1.0. Early stopping: patience 30 epochs. Batch size: 512. Best model saved at epoch 34 with validation loss 0.0162. Training data: 127,078 samples across 74 features (after engineering). Model parameters: 493,657.

---

## Model Performance

### March 3, 2026 Notebook Results

**Validation (2022):**
- RMSE: 145 MWh
- Population-weighted RMSE: 12.4%

**Test (2023):**
- RMSE: 184 MWh
- Population-weighted RMSE: 15.9%

### LightGBM v4 Baseline Comparison (Test 2023)

- ClimateFEAT: RMSE 184 MWh, pop-weighted 15.9%
- LightGBM v4: RMSE 199 MWh, pop-weighted 17.4%

See `climatefeat_model_performance.md` for full error analysis by county, season, demand level, and temperature regime.

---

## Error Analysis Summary

Error analysis shows the model struggles most with LA County (RMSE 1,167 MWh on test, mean bias +138 MWh) and exhibits slight weekend bias (Saturday RMSE 166 vs Tuesday RMSE 124). Error scales with county population as expected — bottom 75% of counties by demand have RMSE of just 27 MWh. The model stopped improving at epoch 34 after 30 patience epochs of no validation improvement.