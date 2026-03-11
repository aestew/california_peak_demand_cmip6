# ClimateFEAT Feature Engineering Documentation

## Overview

ClimateFEAT's feature engineering pipeline transforms raw data from 10 source categories into model-ready features. All engineering is performed before the train/validation/test split to ensure consistent transformations, with the exception of rolling features which are computed within each split to prevent temporal leakage. The final engineered dataset contains 127,078 samples across 74 features.

---

## Target Engineering

The raw target is max_daily_electricity in MWh per county per day. This is transformed in two steps. First, per-capita normalization: max_elec_per_capita = max_daily_electricity / total_pop. This removes the dominant effect of county size so the model learns demand intensity rather than absolute volume. Second, log transformation: max_elec_per_capita_log = log(max_elec_per_capita). The log compresses the long right tail of demand distributions (driven by heat events in large counties) and stabilizes MSE loss during training. Predictions are inverted via exp() and multiplied by total_pop to recover MWh.

---

## Temperature-Derived Features

**Cooling degree days (CDD65 and CDD75):** CDD65_pop measures how many degrees the population-weighted daily temperature exceeds 65°F. CDD75_pop uses a 75°F base, capturing only severe cooling demand. Both are population-weighted so they reflect conditions where people actually live rather than empty desert or mountain areas within a county. CDD75 is specifically used in the Heat Wave stream because it only activates during genuinely hot days.

**Heating degree days (HDD65):** HDD65_pop measures degrees below 65°F, population-weighted. Captures winter heating demand. Less impactful than CDD in California but still significant for northern and inland counties.

**Temperature range (trange_k):** The spread between daily max and min temperature in Kelvin. Large diurnal swings can drive both heating and cooling demand within a single day, particularly in inland valleys.

---

## Dew Point Depression (dpd_k)

This is the most significant engineered feature. It is derived from specific humidity (spfh_peak_kgkg_pop) through a multi-step physical calculation:

### Derivation Steps

**Step 1:** Convert specific humidity to vapor pressure. Given standard atmospheric pressure P = 101,325 Pa and specific humidity w, vapor pressure e = (w × P) / (0.622 + w).

**Step 2:** Convert vapor pressure to dew point temperature in Celsius using the Magnus formula: dpt_c = 243.04 × ln(e / 611.2) / (17.625 − ln(e / 611.2)).

**Step 3:** Convert to Kelvin: dpt_derived_k = dpt_c + 273.15.

**Step 4:** Calculate depression: dpd_k = tmax_k_pop − dpt_derived_k, clipped at zero.

### Interpretation

Large dpd_k values indicate dry conditions (comfortable, less cooling needed). Small dpd_k values indicate high humidity — the air temperature is close to the dew point, meaning high thermal discomfort and increased air conditioning demand even at moderate temperatures. This feature captures the "it's not the heat, it's the humidity" effect that raw temperature alone misses.

---

## Rolling Aggregates

Rolling features capture sustained weather conditions rather than single-day spikes. All are computed per county using groupby-transform to prevent cross-county leakage.

**cdd65_pop_roll5:** 5-day rolling sum of CDD65. A multi-day heat event drives cumulative cooling demand as buildings absorb heat and occupants exhaust their tolerance. The sum (not mean) captures total accumulated thermal stress.

**hdd65_pop_roll5:** 5-day rolling sum of HDD65. Same logic for sustained cold events.

**tmax_k_pop_roll5_max:** 5-day rolling maximum of daily max temperature. Identifies whether the current day sits within a heat wave regardless of day-to-day fluctuations.

**tmax_k_pop_roll7_mean:** 7-day rolling mean of daily max temperature. Smoothed indicator of the general temperature regime over the past week.

**dpd_k_roll5:** 5-day rolling mean of dew point depression. Sustained humidity is more impactful than a single humid day since buildings and occupants take time to respond.

All rolling features use min_periods=1 so the first few days of each county's time series still produce values rather than NaN.

---

## 2017 Baseline Features

**baseline_mw_per_capita_2017:** Annual average per-capita electricity consumption for each county in 2017. This is a static structural feature that anchors the model to each county's fundamental demand profile. A county like Imperial (hot, agricultural, high per-capita demand) has a very different baseline than San Francisco (mild, dense, low per-capita demand). This feature appears in every stream to provide county-level context.

**baseline_mw_monthly_2017:** Monthly variant of the same, capturing the seasonal shape of each county's demand curve in 2017. Some counties have extreme summer peaks (inland Central Valley) while others are relatively flat year-round (coastal).

### Construction

Built by merging 2017 electricity usage data with 2017 population data, computing per-capita consumption at both annual and monthly granularity, then joining back to the main dataset on county (and county + month for the monthly version).

---

## Income Feature

**per_cap_income:** Per capita personal income adjusted for inflation. Missing values are imputed first using the county-level median, then falling back to the global median if the county has no valid income observations. Income proxies for air conditioning prevalence, building quality, and demand elasticity.

---

## Day of Week Encoding

day_of_week is converted from string labels to integers via a mapping built from the unique values in the dataset. The mapping is saved as dow_map in the training artifacts to ensure consistent encoding during inference. This was a significant debugging issue during inference pipeline development — the original dow_map was built from df['day_of_week'].unique() which produces a non-standard ordering (not Monday=0), and this ordering must be exactly reproduced at inference time.

---

## Infrastructure Features — Data Centers

### Historical Data

Data center features are cumulative totals computed per county per year: cuml_count (total number of data centers), cuml_sq_foot (total square footage across all data centers), cuml_utility_cap (sum of maximum MW capacity across individual data centers in the county), and cuml_dc_load (total operational load in MW — roughly how much electricity the data centers actually consume).

Historical data (2016–2024) comes from DataCenters.com facility records aggregated by county and TAC (Transmission Access Charge area: PGE, SCE, or SDGE).

### Future Projections (2025–2040)

For future projections, cuml_utility_cap and cuml_dc_load are projected using percentage growth rates sourced from CEC data center forecasts (the 2024 Final Data Center Forecast and the 2025 IEPR Preliminary Data Center Forecast). Growth rates are applied as multipliers against each county's 2024 baseline values, with rates varying by TAC:

- **PGE:** Grows from +4.39% in 2025 to +96.12% by 2040 (nearly doubling utility capacity). This reflects the massive anticipated data center buildout in Northern California.
- **SCE:** More moderate growth, from +2.75% in 2025 to +34.17% by 2040.
- **SDGE:** Flat — zero projected growth across all years.

The growth rates are applied uniformly to all counties within each TAC. Each county's 2024 actual cuml_utility_cap is multiplied by (1 + growth_rate_pct / 100) for each projected year.

### Derived Projections for Count and Square Footage

For cuml_count and cuml_sq_foot, future values are derived using historical ratios from 2024: count_per_mw (data centers per MW of utility capacity) and sqft_per_mw (square feet per MW). These ratios are calculated per county from 2024 actuals, then multiplied by the projected cuml_utility_cap to back out projected count and square footage. The assumption is that the physical characteristics of data centers (average size, average capacity per facility) remain consistent with 2024 patterns as the fleet grows.

### Daily Expansion and Validation

Annual projections are expanded to daily frequency by merging with a full date range (2025-01-01 through 2040-12-31), so each day in a given year carries that year's projected values. The final combined dataset spans 2016-12-31 through 2040-12-31 with 508,486 rows and zero duplicate county-TAC-date combinations.

All projected rows are flagged with real_data = False to distinguish them from historical observations.

---

## Population Weighting

All spatial climate features exist in two variants: area-mean (simple average across all grid cells in a county) and population-weighted (grid cells weighted by population density). The model uses population-weighted variants for all climate features because they better represent the conditions experienced by electricity consumers. A county like San Bernardino has vast uninhabited desert, so the area-mean temperature is much hotter than what residents in the populated western portion actually experience.

---

## Feature Selection Rationale

Features were selected across model iterations. The LightGBM baseline (v4) used a different subset than ClimateFEAT — for example, LightGBM used unweighted CDD65 and morning dewpoint while ClimateFEAT shifted to all population-weighted variants and the derived dew point depression. The feature dictionary documents which features are used by which model. Key selection decisions include dropping commuting features (discontinued February 2025), dropping area measurements (low signal), and emphasizing population-weighted climate variables over unweighted ones.