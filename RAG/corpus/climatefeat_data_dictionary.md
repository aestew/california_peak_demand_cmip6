# ClimateFEAT Feature Dictionary

## Overview

This document catalogs all raw and engineered features used in the ClimateFEAT project, organized by source category. For each feature, the dictionary specifies the attribute name, description, unit, data source URL, date range, and which models use it. The project uses 73+ raw features across 10 source categories, plus engineered features derived during the feature engineering pipeline.

The two production models are **ClimateFEAT Transformer** (five-stream attention architecture) and **LightGBM v4** (gradient-boosted baseline). An earlier XGBoost model was also trained but is not the current baseline. The "Used in" columns below reflect the March 3, 2026 notebook configurations.

Model performance from March 3, 2026 notebooks: ClimateFEAT Transformer validation RMSE 145 MWh / 12.4% pop-weighted, test RMSE 184 MWh / 15.9% pop-weighted. LightGBM v4 validation RMSE 141 MWh / 12.0% pop-weighted, test RMSE 199 MWh / 17.4% pop-weighted. See `climatefeat_model_performance.md` for full error analysis.

## Source Summary

| Source | Start Date | End Date | Historical URL | Future/Projection Source |
|--------|-----------|---------|---------------|------------------------|
| URMA | 2019-01-01 | 2025-12-31 | https://www.nco.ncep.noaa.gov/pmb/products/rtma/ | https://loca.ucsd.edu/ (LOCA2 CMIP6) |
| Commuting | 2016-12-31 | 2023-12-31 | https://lehd.ces.census.gov/data/#lodes | No longer using as of 2/25 |
| Data Centers | 2016-12-31 | 2025-12-31 | https://www.datacenters.com/locations/united-states/california | CED 2024 Peak Forecast (TN 262286) |
| Electricity | 2016-01-01 | 2023-12-31 | https://catalog.data.gov/dataset/hourly-electricity-demand-profiles-for-each-county-in-the-contiguous-united-states | Target variable — not projected |
| EV Charging | 2020-04-01 | 2025-09-01 | https://www.energy.ca.gov/files/zev-and-infrastructure-stats-data | Not using as of 2/25 |
| EV Population | 2010-01-01 | 2024-01-01 | https://www.energy.ca.gov/files/zev-and-infrastructure-stats-data | https://www.biologicaldiversity.org/programs/climate_law_institute/pdfs/All-Electric-Drive-California-zero-emissions-vehicles-report.pdf |
| Income | 2016-12-31 | 2024-12-31 | https://dof.ca.gov/forecasting/economics/ and https://www.census.gov/programs-surveys/saipe.html | https://dof.ca.gov/forecasting/economics/ |
| Population & Housing | 2016-01-01 | 2025-01-01 | https://dof.ca.gov/forecasting/demographics/estimates/ | Same source (DOF projections) |
| Area | N/A | N/A | https://en.wikipedia.org/wiki/List_of_counties_in_California | Static — not used as of 2/25 |
| Calendar | 2011-01-01 | 2024-12-31 | Python libraries (pandas, holidays) | Generated programmatically |

---

## URMA Weather Features (28 raw features)

All URMA features are derived from the Unrestricted Mesoscale Analysis (URMA) gridded weather product at 2.5 km resolution. Features come in two variants: population-weighted (`_pop` suffix, weighted by WorldPop 1km constrained population regridded to URMA grid) and area-mean (`_mean` suffix, simple spatial average). Population-weighted variants are preferred for demand modeling because they reflect conditions experienced by the population rather than uninhabited terrain.

### Temperature

| Attribute | Full Name | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|------|-------------|-------------|-------------------|
| tmax_k_pop | Max Temperature (Pop-Weighted) | Kelvin | Yes | Yes | Weather-Time |
| tmin_k_pop | Min Temperature (Pop-Weighted) | Kelvin | Yes | Yes | Weather-Time |
| trange_k | Temperature Range | Kelvin | Yes | Yes | Weather-Time |
| tavg_k | Average Temperature | Kelvin | No | No | — |
| tmax_k | Max Temperature (Unweighted) | Kelvin | No | No | — |
| tmin_k | Min Temperature (Unweighted) | Kelvin | No | No | — |

### Degree Days

| Attribute | Full Name | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|------|-------------|-------------|-------------------|
| cdd65_pop | Cooling Degree Days Base 65°F (Pop-Weighted) | Degree-days | Yes | Yes | Weather-Time, Heat Wave |
| hdd65_pop | Heating Degree Days Base 65°F (Pop-Weighted) | Degree-days | Yes | Yes | Weather-Time |
| cdd75_pop | Cooling Degree Days Base 75°F (Pop-Weighted) | Degree-days | Yes | Yes | Weather-Time, Heat Wave |
| cdd65 | CDD Base 65°F (Unweighted) | Degree-days | No | No | — |
| cdd75 | CDD Base 75°F (Unweighted) | Degree-days | No | No | — |
| hdd65 | HDD Base 65°F (Unweighted) | Degree-days | No | No | — |

Degree days are computed at the grid cell level before population-weighted aggregation to county, preserving nonlinear temperature–demand relationships. CDD75 captures extreme cooling demand (degrees above 75°F) and is a key input to the transformer's dedicated Heat Wave stream.

### Humidity

| Attribute | Full Name | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|------|-------------|-------------|-------------------|
| spfh_peak_kgkg_pop | Specific Humidity Peak (Pop-Weighted) | kg/kg | Yes | Yes | Weather-Time |
| spfh_peak_kgkg_mean | Specific Humidity Peak (Area Mean) | kg/kg | No | No | — |
| dpt_afternoon_k_pop | Afternoon Dewpoint (Pop-Weighted) | Kelvin | No | No | — |
| dpt_afternoon_k_mean | Afternoon Dewpoint (Area Mean) | Kelvin | No | No | — |
| dpt_morning_k_pop | Morning Dewpoint (Pop-Weighted) | Kelvin | No | No | — |
| dpt_morning_k_mean | Morning Dewpoint (Area Mean) | Kelvin | No | No | — |

### Wind

| Attribute | Full Name | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|------|-------------|-------------|-------------------|
| wind_peak_ms_pop | Peak Wind Speed (Pop-Weighted) | m/s | Yes | Yes | Weather-Time |
| wind_peak_ms_mean | Peak Wind Speed (Area Mean) | m/s | No | No | — |
| wind_low_ms_pop | Low Wind Speed (Pop-Weighted) | m/s | No | No | — |
| wind_low_ms_mean | Low Wind Speed (Area Mean) | m/s | No | No | — |

### Cloud Cover

| Attribute | Full Name | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|------|-------------|-------------|-------------------|
| cloud_cover_pct_pop | Cloud Cover (Pop-Weighted) | % | No | No | — |
| cloud_cover_pct_mean | Cloud Cover (Area Mean) | % | No | No | — |

### Data Quality

| Attribute | Full Name | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|------|-------------|-------------|-------------------|
| real_data_urma | URMA Data Flag | Boolean | No | No | — |

Indicates whether the row uses real URMA observed weather vs. imputed/modeled data.

---

## Commuting Features (4 raw features)

Derived from LEHD Origin-Destination Employment Statistics (LODES). Commuting data was dropped from production models as of February 25, 2026 but retained in the dataset for potential future use. LightGBM v4 uses a frozen 2019 mobility baseline (median values by county × day_of_week) rather than the raw time-varying commuting features.

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer |
|-----------|-----------|-------------|------|-------------|-------------|
| staying_total | Staying Population | People present in county but not commuting out | Count | No (frozen 2019 baseline used instead) | No |
| entering_total | Entering Population | People commuting into county from elsewhere | Count | No (frozen 2019 baseline used instead) | No |
| leaving_total | Leaving Population | People commuting out of county | Count | No (frozen 2019 baseline used instead) | No |
| real_data_commuting | Commuting Data Flag | Whether commuting figures are observed vs. estimated | Boolean | No | No |

---

## Data Center Features (5 raw features)

Sourced from datacenters.com facility listings, with future projections based on CEC CED 2024 growth rates by Transmission Access Charge (TAC) area. All features are cumulative running totals per county.

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|-------------|------|-------------|-------------|-------------------|
| cuml_count | Cumulative Data Center Count | Running total of data centers in county | Count | Yes | Yes | Infrastructure-Time |
| cuml_sq_foot | Cumulative Data Center Sq Ft | Running total floor area of data centers | Sq ft | Yes | Yes | Infrastructure-Time |
| cuml_utility_cap | Cumulative Utility Capacity | Running total utility-scale generation capacity online | MW | Yes | Yes | Infrastructure-Time |
| cuml_dc_load | Cumulative Data Center Load | Running total estimated electricity load from data centers | MW | Yes | Yes | Infrastructure-Time |
| real_data_data_centers | Data Center Data Flag | Whether data center figures are observed vs. estimated | Boolean | No | No | — |

---

## Electricity Features (1 raw feature — target)

| Attribute | Full Name | Description | Unit | Role |
|-----------|-----------|-------------|------|------|
| electricity_usage (max_daily_electricity) | Electricity Usage | County-level daily maximum hourly electricity demand | MWh | Target variable |

The raw target is transformed to log per-capita form for model training: `max_elec_per_capita_log = log(max_daily_electricity / total_pop)`. Predictions are back-transformed to MWh by `exp(pred) × total_pop` for evaluation.

---

## EV Charging Features (8 raw features)

From CEC ZEV and Infrastructure Stats. Charging features are not currently used in production models as of February 25, 2026.

| Attribute | Full Name | Unit | LightGBM v4 | Transformer |
|-----------|-----------|------|-------------|-------------|
| Public Level 1 | Public Level 1 EV Chargers | Count | No | No |
| Shared Private Level 1 | Shared Private Level 1 EV Chargers | Count | No | No |
| Public Level 2 | Public Level 2 EV Chargers | Count | No | No |
| Shared Private Level 2 | Shared Private Level 2 EV Chargers | Count | No | No |
| Public DC Fast | Public DC Fast Chargers | Count | No | No |
| Shared Private DC Fast | Shared Private DC Fast Chargers | Count | No | No |
| Total | Total EV Chargers | Count | No | No |
| real_data_ev_charging | EV Charging Data Flag | Boolean | No | No |

---

## EV Population Features (4 raw features)

From CEC ZEV registrations data. BEV count is used as an infrastructure feature in both models.

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|-------------|------|-------------|-------------|-------------------|
| BEV | Battery Electric Vehicles | Registered BEV population in county | Count | Yes | Yes | Infrastructure-Time |
| PHEV | Plug-in Hybrid Electric Vehicles | Registered PHEV population in county | Count | No | No | — |
| FCEV | Fuel Cell Electric Vehicles | Registered FCEV population in county | Count | No | No | — |
| real_data_ev_poplution | EV Population Data Flag | Whether EV registration figures are observed vs. estimated | Boolean | No | No | — |

---

## Income Features (2 raw features)

From California Department of Finance and Census Bureau SAIPE.

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|-------------|------|-------------|-------------|-------------------|
| per_capita_personal_income_adjusted (per_cap_income) | Per Capita Personal Income (Adjusted) | Median household income in county, inflation-adjusted | USD | Yes | Yes | Geo-Numeric, Heat Wave |
| real_data_income | Income Data Flag | Whether income figures are observed vs. estimated | Boolean | No | No | — |

Income is imputed using county-level median fill, with fallback to global median, before model training. Zero missing values after imputation.

---

## Population & Housing Features (10 raw features)

From California Department of Finance demographic estimates.

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|-------------|------|-------------|-------------|-------------------|
| total_pop | Total Population | Total county population | Count | Yes | Yes | Geo-Numeric (also used in target denominator) |
| household_pop | Household Population | Population living in households | Count | No | No | — |
| group_quarters_pop | Group Quarters Population | Population in dorms, prisons, nursing facilities | Count | No | No | — |
| total_households | Total Households | Total number of household units | Count | No | No | — |
| single_detached | Single Detached Units | Single-family detached housing units | Count | No | No | — |
| single_attached | Single Attached Units | Single-family attached (townhomes) | Count | No | No | — |
| two_to_four | 2–4 Unit Buildings | Housing units in 2–4 unit buildings | Count | No | No | — |
| five_plus | 5+ Unit Buildings | Housing units in 5+ unit buildings | Count | No | No | — |
| mobile_homes | Mobile Homes | Mobile home units | Count | No | No | — |
| occupied | Occupied Units | Occupied housing units | Count | No | No | — |
| real_data_population | Population Data Flag | Whether population figures are observed vs. estimated | Boolean | No | No | — |

---

## Area Features (1 raw feature)

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer |
|-----------|-----------|-------------|------|-------------|-------------|
| Area | County Area | Geographic area of county | Sq miles | No | No |

Static feature. Not used in production models as of February 25, 2026.

---

## Calendar Features (7 raw features)

Generated programmatically from Python datetime and holidays libraries.

| Attribute | Full Name | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-----------|-------------|------|-------------|-------------|-------------------|
| date | Date | Calendar date | Date | Index (not a feature) | Index (not a feature) | — |
| month | Month | Calendar month (1–12) | Integer | Yes | Yes | Weather-Time, Rolling-Time, Infrastructure-Time |
| quarter | Quarter | Calendar quarter (1–4) | Integer | Yes | Yes | Weather-Time, Rolling-Time, Infrastructure-Time |
| day_of_week | Day of Week | Day name mapped to integer | String → Integer | Yes (categorical) | Yes (mapped via dow_map) | Weather-Time, Rolling-Time, Infrastructure-Time |
| is_holiday | Is Holiday | Whether the date is a US federal holiday | Boolean | Yes | Yes | Weather-Time, Rolling-Time, Infrastructure-Time |
| year | Year | Calendar year | Integer | No | No | — |
| day_of_year | Day of Year | Day number within year (1–366) | Integer | No | No | — |
| holiday | Holiday Name | Name of federal holiday if applicable | String | No | No | — |

**Note on day_of_week encoding:** In the transformer, `day_of_week` is mapped to integers via a `dow_map` derived from `df['day_of_week'].unique()` order, which is data-dependent. The saved map is `{'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Saturday': 5, 'Friday': 6}`. In LightGBM, `day_of_week` is handled as a native categorical feature.

---

## Engineered Features

These features are derived during the feature engineering pipeline and do not appear in the raw source data. See `climatefeat_feature_engineering.md` for derivation details.

### Dew Point Depression

| Attribute | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-------------|------|-------------|-------------|-------------------|
| dpd_k | Dew point depression: tmax_k_pop minus derived dewpoint temperature | Kelvin | Yes | Yes | Weather-Time |
| dpd_k_roll5 | 5-day rolling mean of dpd_k | Kelvin | Yes | Yes | Rolling-Time, Heat Wave |

Derived from specific humidity via: specific humidity → vapor pressure → dew point (Magnus formula) → depression (tmax - dewpoint, clipped at 0). Large values indicate dry conditions, small values indicate humid conditions. Validation statistics: mean 15.18 K, std 8.17 K, range 0–52.18 K.

### Rolling Aggregates

| Attribute | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-------------|------|-------------|-------------|-------------------|
| cdd65_pop_roll5 | 5-day rolling sum of CDD65 (pop-weighted) | Degree-days | Yes | Yes | Rolling-Time |
| hdd65_pop_roll5 | 5-day rolling sum of HDD65 (pop-weighted) | Degree-days | Yes | Yes | Rolling-Time |
| tmax_k_pop_roll5_max | 5-day rolling max of tmax_k_pop | Kelvin | Yes | Yes | Rolling-Time |
| tmax_k_pop_roll7_mean | 7-day rolling mean of tmax_k_pop | Kelvin | Yes | Yes | Rolling-Time |

All rolling features use `min_periods=1` to avoid dropping early-window observations.

### 2017 Baselines

| Attribute | Description | Unit | LightGBM v4 | Transformer | Transformer Stream |
|-----------|-------------|------|-------------|-------------|-------------------|
| baseline_mw_per_capita_2017 | Annual mean per-capita electricity demand in 2017 | MW/person | Yes | Yes | Weather-Time, Rolling-Time, Geo-Numeric, Infrastructure-Time, Heat Wave |
| baseline_mw_monthly_2017 | Monthly mean total electricity demand in 2017 by county | MWh | Yes | Yes | Weather-Time, Rolling-Time, Geo-Numeric, Infrastructure-Time |

2017 baselines anchor each county's demand level without leaking future information into the model. They appear in multiple transformer streams because they provide essential scale context for cross-attention fusion.

### Other Engineered Features (not in current production models)

| Attribute | Description | Unit | Used in older models |
|-----------|-------------|------|---------------------|
| hour_of_max | Hour of day when peak demand occurred | Integer (0–23) | XGBoost |
| per_capita_personal_income_adjusted | Inflation-adjusted per-capita income | USD | XGBoost, LightGBM (as per_cap_income) |

---

## Transformer Stream Assignments

The ClimateFEAT transformer routes features into five parallel attention streams. Several features appear in multiple streams to provide shared context.

| Stream | Embed Dim | Features | Cross-Attention |
|--------|----------|----------|----------------|
| Weather-Time | 32 | tmax_k_pop, tmin_k_pop, trange_k, cdd65_pop, hdd65_pop, cdd75_pop, spfh_peak_kgkg_pop, wind_peak_ms_pop, dpd_k, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017 (15 features) | Yes |
| Rolling-Time | 32 | cdd65_pop_roll5, hdd65_pop_roll5, tmax_k_pop_roll5_max, tmax_k_pop_roll7_mean, dpd_k_roll5, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017 (11 features) | Yes |
| Geo-Numeric | Dense (32-dim output) | total_pop, per_cap_income, baseline_mw_per_capita_2017, baseline_mw_monthly_2017 (4 features + county embedding) | Yes |
| Heat Wave | 64 | baseline_mw_per_capita_2017, per_cap_income, cdd75_pop, dpd_k_roll5, cdd65_pop (5 features) | Yes |
| Infrastructure-Time | 32 | cuml_count, cuml_sq_foot, cuml_utility_cap, cuml_dc_load, bev, month, quarter, day_of_week, is_holiday, baseline_mw_per_capita_2017, baseline_mw_monthly_2017 (11 features) | No — bypasses cross-attention, concatenates directly to prediction head |

The Heat Wave stream uses 2× larger embedding dimensions (64 vs 32) to provide additional capacity for capturing nonlinear heat–demand interactions. The Infrastructure-Time stream bypasses cross-attention and feeds directly into the final prediction head, preventing slow-moving infrastructure trends from interfering with fast weather–demand dynamics in the attention mechanism.

---

## LightGBM v4 Feature List (27 features + county categorical)

The full ordered feature list for LightGBM v4: day_of_week, quarter, month, is_holiday, tmax_k_pop, tmin_k_pop, trange_k, hdd65_pop, cdd65_pop, cdd75_pop, cdd65_pop_roll5, hdd65_pop_roll5, tmax_k_pop_roll5_max, tmax_k_pop_roll7_mean, spfh_peak_kgkg_pop, wind_peak_ms_pop, cuml_count, cuml_sq_foot, cuml_utility_cap, cuml_dc_load, bev, per_cap_income, total_pop, baseline_mw_per_capita_2017, baseline_mw_monthly_2017, dpd_k, dpd_k_roll5. County is handled as a native LightGBM categorical feature (not one-hot encoded).