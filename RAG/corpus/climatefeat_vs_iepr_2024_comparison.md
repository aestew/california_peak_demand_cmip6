# ClimateFEAT vs. CEC 2024 IEPR Update: Methodology Comparison

## Document Scope

This document compares the ClimateFEAT transformer model against the adopted Final 2024 Integrated Energy Policy Report Update electricity demand forecast (CEC-100-2024-001-LCF, adopted January 21, 2025). All CEC-side references are to the adopted forecast only — not proposed 2025 IEPR improvements or future plans. All ClimateFEAT references are to the March 2026 model configuration documented in the project's methodology and performance notebooks.

These are complementary approaches, not competing ones. ClimateFEAT is a research tool designed to explore how nonstationary climate projections affect county-level demand. The CEC forecast is the state's official planning instrument with regulatory authority. The comparison identifies where ClimateFEAT's design choices address specific limitations acknowledged in the 2024 IEPR.

---

## Climate Data and Projections

### CEC 2024 IEPR

- Uses hourly output from **4 WRF models** (CESM2, CNRM-ESM2, EC-Earth3-Veg, FGOALS-g3), all under SSP3-7.0, downscaled and localized to specific weather stations within the CEC's forecast modeling framework.
- 4 additional WRF models became available during the cycle but were **not incorporated**. CEC stated: "The increased warming trend is too significant a change to implement during a forecast update."
- Temperature analysis examines distributions of summer daily tmax for entire utility territories (all of PGE, all of SCE) as single distributions.
- Climate trend is handled through detrended temperature series centered on 2023, producing a stationary weather library. The trend is effectively removed.
- Weather variables in the forecast: HDD and CDD at the planning-area level.
- No humidity variables in the climate/weather inputs to the demand models.

### ClimateFEAT

- Uses **LOCA2 downscaled CMIP6 projections** at 6 km resolution (David Pierce, Scripps; NCA5 input dataset). 4 climate variables: tasmax, tasmin, wind speed, specific humidity.
- Runs inference across **24 SSP3-7.0 ensemble members and 15 SSP2-4.5 members** (11.7M and 7.3M rows respectively), spanning 27 GCMs and 329 total ensemble members in the LOCA2 archive.
- The climate trend is **retained** — projections run forward through 2040 with warming intact, which is the point of a climate-informed forecast.
- Weather features include population-weighted temperature (tmax, tmin, range), CDD at two thresholds (65°F, 75°F), HDD, specific humidity, wind speed, and derived dew point depression — all computed at the grid cell level before county aggregation.
- Historical weather from URMA gridded analysis at 2.5 km resolution, not weather station point observations.

### Why It Matters

The CEC acknowledged warmer projections exist but deferred them. ClimateFEAT is designed specifically for this problem: quantifying demand under nonstationary climate using ensemble projections rather than a detrended stationary library. The CEC's exclusion of humidity variables misses the demand signal from humid heat events, where AC load is driven by the combination of temperature and moisture, not temperature alone.

---

## Spatial Resolution

### CEC 2024 IEPR

- Forecast is produced for **8 planning areas and 20 forecast zones**, corresponding to utility service territories and sub-territories.
- Temperature and econometric relationships are established at the planning-area or forecast-zone level.
- A single temperature distribution represents an entire utility territory (e.g., PGE covers Eureka to Bakersfield in one distribution).

### ClimateFEAT

- Operates at **58 California counties** with daily resolution.
- All weather features are population-weighted at the grid cell level: WorldPop 1 km constrained population is regridded to the URMA 2.5 km grid via KDTree nearest-neighbor mapping, and weather values are aggregated as `sum(value × pop) / sum(pop)` per county per day.
- Degree days are computed at the grid cell before aggregation, preserving the nonlinear temperature-demand relationship that is lost when averaging temperature across large areas first.

### Why It Matters

Population-weighted county-level aggregation means that conditions in heavily populated areas (LA Basin, Bay Area, Sacramento Valley) are not diluted by sparsely populated terrain within the same utility territory. This matters most for heat events, where inland valleys can be 30°F warmer than coastal areas within the same planning zone.

---

## Modeling Architecture

### CEC 2024 IEPR

- **Econometric approach:** Historical correlations between consumption and drivers (income, employment, rates, weather) established per forecast zone and sector, then projected forward.
- Separate model types by sector: residential end-use calibrated by econometric, commercial econometric, industrial/agricultural econometric by NAICS, TCU/streetlighting trend.
- Load modifiers (BTM PV, storage, data centers, AAEE, AAFS, AATE) are computed independently and added/subtracted from the baseline.
- The hourly forecast applies hourly profiles to the annual forecast, with load modifiers layered on using separate profile shapes.
- Additive structure: baseline + data centers − BTM DG − AAEE + AAFS + AATE = managed forecast.

### ClimateFEAT

- **Multi-stream transformer:** Five parallel attention streams (weather-time, rolling-time, geo-numeric, heat wave, infrastructure-time) with cross-attention fusion across four streams. Infrastructure bypasses cross-attention and concatenates directly to the prediction head.
- Learned county embeddings (8-dimensional) prepended as tokens to each stream, allowing the model to learn county-specific climate-demand responses.
- Single end-to-end model predicts daily peak per-capita electricity demand (log-transformed) from all input features simultaneously — no additive decomposition into separate load modifiers.
- Heat wave stream has 2× embedding capacity (64 vs 32 dimensions), giving the model dedicated capacity for nonlinear extreme heat interactions.
- 493,657 parameters. Trained on 84,738 samples (2018–2021, 58 counties × ~365 days).

### Why It Matters

The CEC's additive structure means interactions between climate, infrastructure growth, and electrification must be specified manually or are missed entirely. ClimateFEAT's cross-attention fusion learns these interactions from data. For example, the interaction between rising data center load and rising temperatures — which compound in the same peak hours — is captured implicitly rather than requiring separate analysis.

---

## Data Center Treatment

### CEC 2024 IEPR

- Application-based approach: utility-reported data center applications from 5 utilities, categorized by stage (T&D Planning, Group 1–3).
- Confidence levels applied by scenario: 50–100% depending on application stage.
- 67% utilization factor (from SVP analysis of 60+ existing data centers).
- Load profiles assumed flat (minimal seasonal/daily variability), not necessarily coincident with system peak.
- Load growth flattens after 2035 — no long-term growth rate modeled due to uncertainty.
- Stakeholders commented the projections may be too low.

### ClimateFEAT

- Data center presence is captured through four features in the infrastructure-time stream: cumulative count, cumulative square footage, cumulative utility capacity (MW), and cumulative estimated load (MW).
- Historical data from datacenters.com facility listings. Future projections use CEC CED 2024 growth rates by TAC area (PGE up to +96% by 2040, SCE +34%, SDGE flat), with 2024 ratio-based scaling for count/sqft and daily expansion.
- Data center features interact with all other features through the prediction head — the model learns how data center growth modifies the relationship between weather and demand.
- Infrastructure stream bypasses cross-attention, preventing slow-moving infrastructure trends from interfering with fast weather-demand dynamics.

### Why It Matters

CEC treats data centers as an additive load block layered onto the baseline. ClimateFEAT treats data center growth as a feature that modifies the demand response surface — the model can learn, for example, that a county with high data center load has a different temperature sensitivity than one without.

---

## Humidity and Heat Stress

### CEC 2024 IEPR

- Weather inputs to demand models are HDD and CDD (temperature-only metrics).
- No humidity, dew point, or apparent temperature variables.
- No dedicated handling of compound heat events (high temperature + high humidity).

### ClimateFEAT

- Specific humidity (spfh_peak_kgkg_pop) is a direct input feature, population-weighted.
- Dew point depression (dpd_k) is derived from specific humidity via the Magnus formula: specific humidity → vapor pressure → dew point → depression (tmax − dewpoint, clipped at 0).
- 5-day rolling mean dew point depression (dpd_k_roll5) captures persistence of humid conditions.
- CDD75 (population-weighted cooling degree days above 75°F) is a dedicated extreme heat feature fed to the heat wave stream.
- Validation shows CDD75 correlates at r=0.51 and dpd_k at r=0.46 with log demand in September, confirming both temperature and humidity carry independent signal.

### Why It Matters

A dry 100°F day in the Central Valley produces different AC demand than a humid 95°F day in the LA Basin. Temperature-only metrics miss this distinction. ClimateFEAT's humidity features capture the actual thermal comfort conditions that drive cooling load.

---

## Temporal Dynamics

### CEC 2024 IEPR

- Annual consumption forecast with hourly profiles applied afterward.
- Peak forecasts use weather variants (1-in-2, 1-in-5, 1-in-10) to represent different return periods.
- Climate data detrended to stationary — multi-day heat wave persistence is not modeled as a trend-dependent phenomenon.
- Monthly peak-day profiles used for Slice of Day resource adequacy.

### ClimateFEAT

- Daily resolution: one prediction per county per day (daily peak per-capita demand).
- Rolling aggregates capture multi-day persistence: 5-day CDD sum, 5-day HDD sum, 5-day tmax max, 7-day tmax mean, 5-day dew point depression mean.
- The rolling-time stream processes these temporal features through self-attention, then cross-attention fuses them with instantaneous weather.
- Under inference, the model produces daily demand for every county across every ensemble member through 2040, generating a full distribution of outcomes rather than point estimates with weather variants.

### Why It Matters

Multi-day heat wave accumulation — where Day 3 of a heat wave produces higher demand than Day 1 at the same temperature because buildings haven't cooled overnight — is captured by the rolling features. The CEC's approach of applying hourly profiles to annual totals cannot represent this dynamic.

---

## Ensemble and Uncertainty

### CEC 2024 IEPR

- 4 WRF models provide climate inputs, all under SSP3-7.0.
- Uncertainty is represented through peak weather variants (1-in-2, 1-in-5, 1-in-10) and scenario combinations (low/mid/high for data centers, BTM DG).
- No multi-scenario SSP comparison.

### ClimateFEAT

- 24 SSP3-7.0 and 15 SSP2-4.5 ensemble members from LOCA2.
- Scenario comparison: SSP3-7.0 (high emissions) vs SSP2-4.5 (moderate mitigation) reveals that demand trajectories converge through ~2040 (~49k → ~70k MWh per-capita statewide, ~40% increase regardless of pathway), diverging only after 2040.
- Sensitivity analysis: 4 frozen-feature runs per scenario isolate climate signal from infrastructure growth (data centers, BEVs).
- Key finding: an interaction term of approximately −11k MWh by 2040 exists between climate and infrastructure features, demonstrating that the nonlinear cross-attention architecture prevents clean additive decomposition. This is a feature, not a bug — it captures real-world interactions the additive approach cannot.

### Why It Matters

ClimateFEAT's ensemble approach generates a distribution of demand futures per county, per day, across climate models and emission scenarios. The CEC uses a small number of deterministic weather variants. ClimateFEAT's scenario convergence finding — that near-term infrastructure planning is largely scenario-independent through 2040 — is directly actionable for CEC planning horizons.

---

## Performance Context

These are not directly comparable numbers because the models forecast different quantities at different scales. ClimateFEAT predicts daily county-level peak per-capita demand; the CEC forecast predicts annual consumption and hourly system load at the planning-area level. The numbers below characterize ClimateFEAT's accuracy on historical data.

### ClimateFEAT Transformer (March 2026 notebooks)

- Validation (2022): RMSE 145 MWh, pop-weighted RMSE 12.4%
- Test (2023): RMSE 184 MWh, pop-weighted RMSE 15.9%
- Outperforms LightGBM v4 baseline on test: 184 vs 199 MWh RMSE, 15.9% vs 17.4% pop-weighted

### CEC 2024 IEPR

- The CEC does not publish comparable county-level daily RMSE metrics. Forecast accuracy is assessed through comparison with actual sales data in subsequent IEPR cycles, and through peak forecast benchmarking against weather-normalized peaks.

---

## Summary of Key Differences

| Dimension | CEC 2024 IEPR | ClimateFEAT |
|-----------|--------------|-------------|
| Climate models | 4 WRF (detrended, stationary) | 24+ CMIP6 ensemble (trend retained) |
| Emission scenarios | SSP3-7.0 only | SSP3-7.0 and SSP2-4.5 |
| Spatial resolution | 8 planning areas / 20 zones | 58 counties |
| Weather aggregation | Weather station point obs | 2.5 km gridded, population-weighted |
| Humidity | Not included | Specific humidity, dew point depression, rolling |
| Degree day computation | Planning-area level | Grid cell level before aggregation |
| Architecture | Sector econometric + additive load modifiers | Multi-stream transformer with cross-attention |
| Data center handling | Additive load block from applications | Learned feature in infrastructure stream |
| Temporal resolution | Annual consumption + hourly profiles | Daily county-level predictions |
| Heat wave persistence | Not explicitly modeled | Rolling 5-day and 7-day aggregates |
| Forecast target | Managed system sales and peak (GWh, MW) | Daily per-capita peak demand (log MWh) |

---

## Source Documents

- CEC: Final 2024 Integrated Energy Policy Report Update. CEC-100-2024-001-LCF. Docket 24-IEPR-01, TN 266141.
- ClimateFEAT: Mar_3_txfrm_attn_9pm__4_.ipynb (transformer training), Mar_3_1103pm_LightGBM.ipynb (baseline), and RAG corpus documents (climatefeat_methodology.md, climatefeat_feature_engineering.md, climatefeat_ssp_scenario_comparison.md, climatefeat_data_pipeline.md, climatefeat_model_performance.md, climatefeat_feature_dictionary.md).