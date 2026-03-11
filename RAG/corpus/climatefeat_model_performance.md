# ClimateFEAT Model Performance

## Overview

This document provides detailed error analysis for the ClimateFEAT transformer model and the LightGBM v4 baseline, including breakdowns by county population, demand level, season, day of week, and temperature regime. All metrics were computed from the March 3, 2026 training notebooks. The primary evaluation metric is population-weighted RMSE as a percentage of population-weighted mean demand, which accounts for the fact that large counties dominate total state demand.

## Headline Metrics

### ClimateFEAT Transformer

- **Validation (2022):** RMSE 145 MWh, pop-weighted RMSE 12.4%
- **Test (2023):** RMSE 184 MWh, pop-weighted RMSE 15.9%
- **Best validation loss:** 0.0162 (MSE on log per-capita target)
- **Training stopped at epoch 34** (patience 30, exhausted)
- **Model parameters:** 493,657

### LightGBM v4

- **Validation (2022):** RMSE 141 MWh, pop-weighted RMSE 12.0%
- **Test (2023):** RMSE 199 MWh, pop-weighted RMSE 17.4%
- **Best iteration:** 2,911 (of 5,000 max, early stopping patience 50)
- **Validation RMSE in log space:** 0.1228

### Head-to-Head Comparison (Test 2023)

| Metric | ClimateFEAT Transformer | LightGBM v4 |
|--------|------------------------|-------------|
| RMSE (MWh) | 184 | 199 |
| Pop-weighted RMSE (%) | 15.9% | 17.4% |

The transformer outperforms LightGBM on the population-weighted metric by 1.5 percentage points on held-out 2023 data. Both models show a generalization gap between validation (2022) and test (2023), with LightGBM degrading more (12.0% → 17.4%) than the transformer (12.4% → 15.9%), suggesting the transformer's multi-stream attention architecture generalizes better to unseen years.

## Population-Weighted RMSE Definition

The primary metric is defined as:

```
pop_weighted_rmse_pct = 100 × sqrt(sum(pop_i × (actual_i - pred_i)²) / sum(pop_i)) / weighted_mean_demand
```

where `weighted_mean_demand = sum(pop_i × actual_i) / sum(pop_i)`. This ensures that prediction quality in Los Angeles (pop ~10M) matters more than prediction quality in Alpine County (pop ~1,100), reflecting the reality that grid planning is dominated by large load centers.

## Error by Demand Level (Validation 2022, Transformer)

| Demand Quartile | Threshold (MWh) | RMSE (MWh) |
|----------------|-----------------|------------|
| Bottom 25% | ≤ 53 | 4 |
| Bottom 50% | ≤ 205 | 11 |
| Bottom 75% | ≤ 664 | 27 |
| Full dataset | ≤ 16,651 | 145 |

Error scales roughly proportionally with demand magnitude. The model achieves very low absolute error on small rural counties (RMSE 4 MWh for the bottom quartile) and the bulk of the aggregate RMSE comes from the largest counties. This is expected behavior for a log per-capita target: percentage errors are roughly uniform, but absolute MWh errors are much larger for counties with high total demand.

## Error by County Population (Validation 2022, Transformer)

| Population Threshold | RMSE (MWh) |
|---------------------|------------|
| ≥ 47,350 (75th %ile) | 169 |
| ≥ 185,183 (50th %ile) | 205 |
| ≥ 697,581 (25th %ile) | 283 |
| ≥ 9,852,298 (LA only) | 910 |

Los Angeles County dominates the error budget. With a population of ~10 million, even small percentage errors translate to large absolute MWh residuals. The model's RMSE for LA alone is 910 MWh on validation, roughly 6x the statewide average.

## Los Angeles County Deep Dive

### Validation (2022)

- **Mean actual demand:** Summer 12,434 MWh, other months lower
- **Mean predicted demand:** Summer 12,964 MWh
- **Summer RMSE:** 1,025 MWh
- **Extreme days (>10k MWh):** 85 days; actual mean 12,664, predicted mean 13,063
- **All other counties summer 2022:** actual 624 MWh, predicted 639 MWh, RMSE 83 MWh

### Test (2023)

- **Mean actual:** 10,375 MWh
- **Mean predicted:** 10,514 MWh
- **RMSE:** 1,167 MWh
- **Bias:** +138 MWh (slight over-prediction)

### LA Monthly Bias (Validation 2022, Transformer)

| Month | Bias (MWh) | RMSE (MWh) |
|-------|-----------|------------|
| Jan | +775 | 1,064 |
| Feb | +581 | 980 |
| Mar | +405 | 1,077 |
| Apr | +157 | 877 |
| May | -67 | 861 |
| Jun | +169 | 557 |
| Jul | -754 | 1,017 |
| Aug | -216 | 603 |
| Sep | -623 | 1,333 |
| Oct | -150 | 566 |
| Nov | +326 | 918 |
| Dec | -142 | 750 |

The transformer tends to over-predict LA demand in winter (positive bias Jan–Mar) and under-predict in late summer (negative bias Jul, Sep). September shows the highest RMSE (1,333 MWh), which aligns with the September 2022 heat wave event. The worst single prediction was September 10, 2022 (actual 9,573 MWh, predicted 14,113 MWh, error 4,539 MWh), a day with elevated CDD75 (4.77) and peak temperatures around 309.6 K (~97°F pop-weighted).

### LA Monthly Bias (Validation 2022, LightGBM v4)

| Month | Avg Actual | Avg Predicted | Bias (MWh) | RMSE (MWh) |
|-------|-----------|--------------|-----------|------------|
| Jan | 9,445 | 8,870 | +576 | 892 |
| Feb | 9,488 | 8,975 | +513 | 980 |
| Mar | 9,394 | 9,027 | +366 | 1,003 |
| Apr | 9,670 | 9,136 | +534 | 1,025 |
| May | 9,724 | 9,181 | +542 | 973 |
| Jun | 11,550 | 11,087 | +462 | 680 |
| Jul | 11,579 | 11,986 | -407 | 721 |
| Aug | 13,028 | 13,276 | -248 | 473 |
| Sep | 12,704 | 12,823 | -119 | 938 |
| Oct | 10,325 | 9,625 | +699 | 1,070 |
| Nov | 9,061 | 8,802 | +259 | 857 |
| Dec | 8,729 | 8,894 | -164 | 789 |

LightGBM shows a persistent positive bias across most months (under-predicting is less common), particularly in shoulder months (Apr–May, Oct). Both models struggle with September heat events, though the transformer's September error is larger (1,333 vs 938 MWh RMSE).

## Statewide Monthly Performance (Test 2023, Transformer)

| Month | Avg Actual (MWh) | Avg Predicted (MWh) | Bias (MWh) | RMSE (MWh) |
|-------|-----------------|--------------------|-----------|-----------| 
| Jan | 648 | 621 | +27 | 205 |
| Feb | 678 | 626 | +52 | 246 |
| Mar | 688 | 636 | +52 | 247 |
| Apr | 667 | 648 | +19 | 177 |
| May | 689 | 678 | +10 | 143 |
| Jun | 701 | 706 | -4 | 114 |
| Jul | 821 | 854 | -33 | 159 |
| Aug | 826 | 866 | -39 | 170 |
| Sep | 742 | 785 | -43 | 175 |
| Oct | 691 | 702 | -11 | 165 |
| Nov | 641 | 633 | +8 | 168 |
| Dec | 626 | 628 | -2 | 202 |

The best months are June (RMSE 114) and May (RMSE 143). The largest RMSE months are February and March (246–247 MWh), likely driven by winter heating variability. Summer months show a slight negative bias (over-prediction), consistent with the model learning from 2018–2021 training data where summers averaged 801 MWh versus 2023's slightly cooler summer at 797 MWh.

## Error by Day of Week (Validation 2022, Transformer)

| Day | RMSE (MWh) | Bias (MWh) |
|-----|-----------|-----------|
| Mon | 146 | +0 |
| Tue | 124 | -2 |
| Wed | 141 | +3 |
| Thu | 143 | +4 |
| Fri | 160 | -9 |
| Sat | 166 | +10 |
| Sun | 132 | +9 |

Weekend days (Fri–Sat) show slightly higher RMSE, which may reflect more variable residential-driven demand patterns on weekends. Bias is near zero across all days, indicating no systematic day-of-week miscalibration.

## Error by Temperature Regime (Validation 2022, Transformer)

| Regime | RMSE (MWh) |
|--------|-----------|
| Cold days (tmin < 10th percentile) | 27 |
| Normal days | 154 |
| Hot days (tmax > 90th percentile) | 143 |

Cold days have very low RMSE because they tend to coincide with small-county, low-demand observations. Hot days (RMSE 143) are slightly better than normal days (RMSE 154), suggesting the heat wave stream and CDD75/DPD features are providing useful signal for extreme heat events.

## September Heat Wave Analysis (Validation 2022)

September 2022 included a significant California heat event. Feature diagnostics for September:

- **CDD75 (pop-weighted):** mean 2.0, max 13.5
- **Dew point depression (dpd_k):** mean 19.13 K, min 1.70 K
- **Rolling dpd_k (5-day):** mean 19.24 K
- **Correlation with log demand:** CDD75 r=0.510, DPD r=0.457

For LA specifically in September: actual demand ranged 9,115–16,651 MWh, predictions ranged 11,006–16,587 MWh, with a mean bias of 623 MWh (over-prediction). The model captures the shape of heat-driven demand spikes but tends to over-respond to extreme CDD75 values, particularly on September 10 when the error reached 4,539 MWh.

## Worst 20 Predictions (Validation 2022, Transformer)

All 20 worst predictions are for Los Angeles County. The largest errors fall into two categories:

1. **Heat event over-prediction:** September 10 (error 4,539 MWh), July 2 (2,058 MWh), July 24 (1,973 MWh) — the model over-responds to high CDD75 on days when actual demand was lower than temperature alone would suggest (possible demand response, cloud cover, or weekend effects).

2. **Cool-season under-prediction:** February 25 (error 2,003 MWh), January 28 (1,941 MWh), November 11 (1,636 MWh) — actual demand was higher than predicted on winter days, suggesting the model is missing some non-climate driver (possibly holiday effects, economic activity, or baseline load shifts).

## Validation vs Test Distribution Check

| Split | Mean (MWh) | Std (MWh) | Summer Avg | Winter Avg |
|-------|-----------|----------|-----------|-----------|
| Train (2018–2021) | — | — | 801 | — |
| Val (2022) | 703 | 1,526 | 828 | 640 |
| Test (2023) | 702 | 1,519 | 797 | 650 |

The validation and test distributions are very similar in aggregate (mean ~702 MWh, std ~1,520 MWh). The 2022 summer was slightly warmer than average (828 vs training average 801), while 2023 summer was slightly cooler (797). This modest distribution shift does not fully explain the 3.5 percentage point degradation from validation to test pop-weighted RMSE (12.4% → 15.9%), suggesting some temporal non-stationarity the model has not captured.

## Training Configuration Summary

### ClimateFEAT Transformer

- **Architecture:** Five parallel stream encoders (weather, rolling, geo, heat wave, infrastructure) with cross-attention fusion across four streams (infrastructure bypasses cross-attention and concatenates directly to the head)
- **Embed dims:** 32 for weather/rolling/infrastructure streams, 64 for heat wave stream, 64 for cross-attention dimension
- **County embedding:** Learned 8-dimensional embedding, prepended as a token to each attention stream
- **Attention:** 8 heads per stream, 2 attention blocks per stream encoder
- **Head:** 640-dim input → 256 → 64 → 1 (with ReLU + dropout 0.2/0.1)
- **Optimizer:** AdamW, lr=3e-4, weight_decay=1e-3
- **Scheduler:** ReduceLROnPlateau (patience 5, factor 0.5)
- **Loss:** MSE on log per-capita demand
- **Batch size:** 512
- **Early stopping:** Patience 30 on validation loss
- **Training data:** 84,738 samples (2018–2021, 58 counties × ~365 days × 4 years)

### LightGBM v4

- **Features:** 27 (plus county as categorical)
- **Key hyperparameters:** n_estimators=5000, learning_rate=0.02, num_leaves=64, min_child_samples=50, subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1, reg_lambda=1.0
- **Target:** log per-capita daily max electricity demand
- **Categorical features:** county, day_of_week (native LightGBM categorical handling)

## Feature Groups (Transformer Streams)

### Weather-Time Stream (15 features)
tmax_k_pop, tmin_k_pop, trange_k, cdd65_pop, hdd65_pop, cdd75_pop, spfh_peak_kgkg_pop, wind_peak_ms_pop, dpd_k, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017

### Rolling-Time Stream (11 features)
cdd65_pop_roll5, hdd65_pop_roll5, tmax_k_pop_roll5_max, tmax_k_pop_roll7_mean, dpd_k_roll5, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017

### Geo-Numeric Stream (4 features, dense path)
total_pop, per_cap_income, baseline_mw_per_capita_2017, baseline_mw_monthly_2017

### Heat Wave Stream (5 features, 64-dim embed)
baseline_mw_per_capita_2017, per_cap_income, cdd75_pop, dpd_k_roll5, cdd65_pop

### Infrastructure-Time Stream (11 features, bypasses cross-attention)
cuml_count, cuml_sq_foot, cuml_utility_cap, cuml_dc_load, bev, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017

## Known Limitations and Error Patterns

1. **LA dominance:** Los Angeles County accounts for all 20 worst predictions and the bulk of aggregate RMSE. Any improvement to LA predictions would substantially reduce the headline metric.

2. **September heat events:** The model over-responds to extreme CDD75 in LA during September, producing the single largest error (4,539 MWh on Sep 10, 2022). This may reflect the model conflating population-weighted CDD with actual experienced cooling demand, which can be modulated by coastal vs inland microclimate differences within the county.

3. **Winter under-prediction in LA:** Several of the worst errors are winter days where actual demand exceeded predictions by 1,600–2,000 MWh, suggesting the model underweights non-climate drivers of winter demand in large urban counties.

4. **Val-to-test degradation:** Both models degrade from validation to test, but the gap is modest (3.5 pp for transformer, 5.4 pp for LightGBM). The transformer's better generalization may stem from its multi-stream attention architecture learning more transferable feature interactions than LightGBM's boosted splits.

5. **Day-of-week encoding:** The transformer notebook uses a non-standard `dow_map` derived from `df['day_of_week'].unique()` ordering, which is data-dependent and not guaranteed to be Monday=0. The saved dow_map was `{'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Saturday': 5, 'Friday': 6}`. This artifact was identified and addressed during inference pipeline development but represents a reproducibility concern if the pipeline is rerun on differently-ordered data.

## Source Notebooks

- `Mar_3_txfrm_attn_9pm__4_.ipynb` — ClimateFEAT transformer training, evaluation, and error analysis
- `Mar_3_1103pm_LightGBM.ipynb` — LightGBM v4 baseline training, SHAP analysis, and test evaluation
- Both notebooks logged to MLflow with full artifacts for reproducibility