# CEC 2024 IEPR Update: Demand Forecast Methodology

## Document Scope

This document summarizes the electricity demand forecasting methodology used in the Final 2024 Integrated Energy Policy Report Update (CEC-100-2024-001-LCF, September 2025, Docket 24-IEPR-01). All content is drawn from Chapter 1 of the adopted report. This document is intended to support comparison with ClimateFEAT's approach to forecasting county-level electricity demand under climate change.

Citation: Bailey, Stephanie, Mathew Cooper, Quentin Gee, Heidi Javanbakht, Jake McDermott, and Danielle Mullany. 2024. Final 2024 Integrated Energy Policy Report Update. California Energy Commission. Publication Number: CEC-100-2024-001-LCF.

---

## Institutional Context

The California Energy Demand Forecast is developed by the CEC and updated annually through the IEPR process. It feeds directly into the CPUC's integrated resource plan (IRP) and resource adequacy (RA) processes, and the California ISO's transmission planning process (TPP). A 2022 MOU between CEC, CPUC, and California ISO established that specific elements of the forecast set will be used for planning and procurement across these proceedings.

The forecast covers annual consumption and sales to 2040 for electricity by customer sector, eight planning areas, and 20 forecast zones. It also includes annual peak electric system load with different weather variants, and annual projections of PV, storage, EVs, energy efficiency, and electrification.

The 2024 IEPR Update is a limited-change update to the 2023 IEPR forecast, using one additional year of historical sales data, updated economic/demographic projections, and updated rate projections.

---

## High-Level Forecast Method

The CEC forecast is fundamentally an econometric approach. Historical energy consumption is correlated with economic/demographic data, weather data, and electricity rates for each forecast zone and economic sector. Those correlations are then extended forward using projections of the same drivers. Load modifiers (BTM PV, storage, data centers, energy efficiency, fuel substitution, transportation electrification) are applied as adjustments to this baseline.

The forecast produces two primary managed scenarios:

- **Planning Forecast:** Used for resource adequacy and integrated resource planning. Mid-level assumptions for BTM PV/storage, data centers, AAEE Scenario 3, AAFS Scenario 3, AATE Scenario 3.
- **Local Reliability Scenario:** Used for transmission planning local area studies and distribution planning. Low BTM PV (less self-generation), high data center load, AAEE Scenario 2 (less efficiency), AAFS Scenario 4 (more fuel substitution). Results in higher demand than the planning forecast.

### Spatial Resolution

The forecast operates at the level of **8 planning areas and 20 forecast zones**, corresponding roughly to utility service territories and sub-territories (PGE, SCE, SDGE, LADWP, SMUD, NCNC, IID, BUGL). Temperature distributions and econometric relationships are established at the planning-area or forecast-zone level.

### Sector Models

The CEC uses separate model types by sector:

- **Residential:** End-use model calibrated by econometric model
- **Commercial:** Econometric model (with plans to update to a modern platform using 2018–2022 Commercial End-Use Survey data)
- **Industrial/Agricultural:** Econometric models by NAICS code
- **Transportation/Communications/Utilities (TCU) and Streetlighting:** Trend analysis

Each sector model establishes historical correlations between consumption and drivers (income, employment, rates, weather, etc.) and projects forward.

---

## Climate and Weather Data

### Historical Weather

The CEC uses weather station data correlated with historical electricity consumption. Weather variables include heating degree days (HDD) and cooling degree days (CDD) calculated at the planning-area level.

### Climate Projections for the Forecast

The 2024 IEPR Update uses hourly output from **4 WRF (Weather Research and Forecasting) models** localized to specific weather stations within the CEC's forecast modeling framework. These models were the same ones used in the 2023 IEPR:

- CESM2 r11i1p1f1
- CNRM-ESM2 r1i1p1f2
- EC-Earth3-Veg r1i1p1f1
- FGOALS-g3 r1i1p1f1

### New WRF Models — Available but NOT Used

Four additional downscaled WRF model runs became available during the 2024 IEPR Update cycle:

- EC-Earth3 r1i1p1f1
- MIROC6 r1i1p1f1
- MPI-ESM1-1-HR r3i1p1f1
- TaiESM1 r11i1p1f1

These new models show significantly higher annual CDD and lower annual HDD compared to the models used in the 2023 IEPR. The CEC explicitly stated: **"The increased warming trend is too significant a change to implement during a forecast update and requires further review by staff and stakeholders."** Staff will explore incorporating the new WRF output beginning with the full 2025 IEPR forecast.

### Temperature Handling

CEC staff produces detrended temperature series centered on 2023 and compares them to the 30-year historical record at the planning-area level. The analysis examines distributions of summer daily maximum temperature for entire utility territories (e.g., all of PGE, all of SCE) as single distributions. This detrending approach effectively removes the climate trend to produce a stationary weather library.

### Peak Weather Variants

Peak demand forecasts are produced under multiple weather variants:

- 1-in-2 (used for resource adequacy, IRP)
- 1-in-5 (used for California ISO TPP policy and bulk system studies)
- 1-in-10 (used for local area reliability studies)

---

## Data Center Methodology

The 2024 IEPR Update moved away from historical-trend-based data center forecasting. Instead, staff used application data from five utilities: Silicon Valley Power, City of Palo Alto, City of San Jose, PG&E, and SCE. Staff also spoke with LADWP, SMUD, and SDG&E and determined data center growth was not significant in those regions.

### Application Categories

PG&E and SCE applications were categorized by stage:

- **T&D Planning:** Completed engineering studies, in development process
- **Group 1:** Active application with completed or to-be-completed engineering study
- **Group 2:** Active application prior to engineering study
- **Group 3:** Project inquiries demonstrating interest but no formal application

### Confidence Levels by Scenario

| Application Stage | Low | Mid | High |
|-------------------|-----|-----|------|
| T&D Planning | 100% | 100% | 100% |
| Group 1 | 50% | 70% | 70% |
| Group 2 | — | 50% (SCE); PG&E not included | 50% |
| Group 3 | — | — | PG&E 10%; SCE 10–50% |

A **67% utilization factor** was applied to convert requested capacity to estimated peak load, based on Silicon Valley Power's analysis of 60+ existing data centers.

### Growth Profile

Data center peak demand annual growth: ~15% (low), ~19% (mid), ~20% (high) from 2024–2030. Nearly 63% of load growth by 2040 is in PGE territory. Load growth flattens after 2035 because staff did not model a long-term growth rate due to high uncertainty.

Data centers alone add more than 3,000 MW to California ISO peak demand by 2040 in the planning forecast.

### Stakeholder Feedback

Many commenters stated projections may be too low, citing missing new applications, no long-term growth modeling, and no redundancy accounting for cross-state load shifting.

---

## BTM Distributed Generation and Storage

### Historical Data Updates

Staff updated historical BTM PV capacity through 2023, resulting in a ~4% (500 MW) increase in cumulative statewide capacity for 2022 vs. the 2023 IEPR. By end of 2023, estimated BTM PV capacity was 17.2 GW.

### Capacity Factors — Significant Revision Downward

Staff revised BTM PV capacity factors using metered generation data from a large real-world sample. The new capacity factors are **3 to 4 percentage points lower** than those used in the 2023 IEPR:

| Year | 2023 IEPR | 2024 IEPR Update |
|------|-----------|------------------|
| 2018 | 21.2% | 18.1% |
| 2019 | 20.3% | 17.4% |
| 2020 | 20.8% | 17.8% |
| 2021 | 21.0% | 18.0% |
| 2022 | 21.6% | 18.5% |

This revision reduced annual BTM PV generation estimates by 1,400 to 2,400 GWh. At peak generation hour (Hour 12), September 2022 generation was 1,000 MW less than previously estimated.

### Adoption Scenarios

Three scenarios (low/mid/high) distinguished by capital expenditure cost assumptions (from NREL 2024 Annual Technology Baseline) and Investment Tax Credit duration:

- **Low:** High capex, ITC ends 2034
- **Mid:** Mid capex, ITC ends 2034
- **High:** Low capex, ITC ends 2042

BTM PV paired with storage increased to 69% of residential NBT interconnections in the first 10 months of 2024, driven by NBT incentive design encouraging evening export.

---

## Load Modifiers: Efficiency, Fuel Substitution, Transportation

### Additional Achievable Energy Efficiency (AAEE)

Six scenarios (1–6) ranging from firm commitments to speculative programs. Scenario 3 used for the planning forecast. AAEE 3 saves approximately 13,500 GWh by 2040 across all sectors.

### Additional Achievable Fuel Substitution (AAFS)

Six scenarios incorporating zero-emission appliance standards (CARB, BAAQMD, SCAQMD). The ZE standard component of AAFS dominates the electricity impact — adding roughly 25 times more electricity than programmatic AAFS 3 by 2040.

Net impact: AAEE + AAFS combined add more electricity than they save starting in 2029 (planning forecast) or 2027 (local reliability scenario). Net increase of ~28,800 GWh by 2040 in the planning forecast.

The planning forecast and local reliability scenario appear to achieve the goal of 6 million heat pumps installed by 2030 (from programmatic and ZE Standard AAFS combined with the estimated 1.5 million existing heat pumps as of 2023).

### Additional Achievable Transportation Electrification (AATE)

One scenario (AATE 3). By 2035: 14.6 million light-duty ZEVs (vs 7.4 million in baseline), ~440,000 medium- and heavy-duty ZEVs. AATE 3 adds approximately 44,000 GWh by 2040.

As of 2023, California had more than 1.5 million ZEVs. New vehicle sales are approximately 25% ZEV.

---

## Economic and Demographic Inputs

All projections from Moody's Analytics and California Department of Finance:

- **Population:** 39.2 million (2024) → 41.3 million (2040), 0.3% annual growth. Higher than 2023 IEPR (0.2%) due to return to normal migration patterns.
- **Households:** 13.9 million (2024) → 15.2 million (2040), 0.6% annual growth.
- **Per capita income:** $80,000 (2024) → $108,300 (2040), 1.8% annual growth. Slower than 2023 IEPR.
- **Gross state product:** $3.9 trillion (2024) → $5.3 trillion (2040), 1.8% annual growth. Slower than 2023 IEPR.
- **Commercial employment:** 0.3% annual growth, 4.1% total increase to 2040.

Electricity rates have risen significantly faster than inflation since 2021, driven by wildfire mitigation costs, rising generation capacity prices, and NEM impacts on IOU rates.

---

## Headline Forecast Results (2040)

| Metric | Planning Forecast | Local Reliability Scenario |
|--------|------------------|---------------------------|
| Baseline Consumption (GWh) | 395,870 | 400,892 |
| BTM DG and Storage (GWh) | 57,562 | 53,267 |
| Baseline Sales (GWh) | 338,309 | 347,626 |
| AAEE (GWh saved) | 13,528 | 10,301 |
| AAFS (GWh added) | 42,288 | 38,777 |
| AATE (GWh added) | 44,053 | 44,053 |
| **Managed Sales (GWh)** | **411,121** | **420,154** |
| California ISO Peak (MW) | 66,798 | 68,519 |

Baseline sales in 2040 are 13% (planning) to 16% (local reliability) higher than the 2023 IEPR, primarily due to data center growth and reduced BTM PV generation assumptions. The 2024 IEPR Update peak forecast is 11.3% higher than the 2023 IEPR planning forecast in 2040.

### Hourly Forecast Changes

The 2024 IEPR Update moved the California ISO system peak from July (2023 IEPR) to September. SDG&E planning area coincidence improved from as low as 82% to roughly 96%, better aligned with historical observations.

---

## Planned Improvements (2025 IEPR and Beyond)

- Developing a probabilistic hourly electricity dataset for resource planning
- Revisiting data center load growth assumptions
- Exploring incorporating utility known-load data from distribution system planning
- Improved geographic assignment of EV load across forecast zones
- Exploring new WRF model output and solar irradiance projections
- Updating commercial sector end-use model with 2018–2022 survey data
- Agriculture vehicle inventory survey integration
- Exploring increased geographic granularity for local studies
- Exploring demand flexibility tools

---

## Key CEC Staff and Contacts (from IEPR)

- **Heidi Javanbakht** — Lead, demand forecast overview and forecast use in planning
- **Nick Fugate** — Climate change impacts on hourly demand forecast; hourly electricity demand
- **Lake Worku** — Weather and climate data in annual consumption models
- **Mathew Cooper** — Annual consumption and sales forecast results
- **Jenny Chen** — Data center forecasts
- **Mark Palmere / Alex Lonsdale** — BTM distributed generation forecast
- **Nicholas Janusch / Ethan Cooper** — AAFS draft results
- **Andre Freeman / Namita Saxena / Farzana Kabir** — Transportation energy demand forecast
- **Sandra Nakagawa** — IEPR Director

---

## Source

Final 2024 Integrated Energy Policy Report Update. CEC-100-2024-001-LCF. Docket 24-IEPR-01, TN 266141. Adopted January 21, 2025. Published September 2025.