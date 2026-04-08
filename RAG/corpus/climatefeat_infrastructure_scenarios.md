# ClimateFEAT Infrastructure Scenario Comparison

## Overview

ClimateFEAT runs six infrastructure scaling scenarios across two SSP climate pathways (SSP3-7.0 and SSP2-4.5) to decompose the drivers of California peak electricity demand growth through 2040. Each scenario modifies data center (DC) and battery electric vehicle (BEV) growth trajectories while holding all other inputs constant, enabling attribution of demand growth to weather/climate, EV adoption, and data center expansion.

All scenarios use the same trained multi-stream transformer model, the same 24-member (SSP3-7.0) and 15-member (SSP2-4.5) CMIP6 ensemble, and the same LOCA2-downscaled weather projections. Infrastructure features are scaled linearly from 1.0× at 2023 to the target factor at 2040, applied before model standardization and inference.

---

## Data Center Scaling

### Source Data

DC growth targets come from the CEC Integrated Energy Policy Report data center forecasts:

- **Low (3,644 MW):** 2024 IEPR Low case. Counts only T&D Planning stage projects (engineering complete, under construction) at 100% confidence. No Group 1, 2, or 3 applications included. Source: CEC Data Center Forecast Final, March 2025 (TN 262286). https://www.energy.ca.gov/sites/default/files/2025-03/Data_Center_Forecast_Final_ada.pdf

- **Mid (4,123 MW):** ClimateFEAT bottom-up pipeline estimate from datacenters.com facility data, scaled by CEC CED 2024 TAC-level growth rates. Approximately matches CEC 2025 IEPR Mid case (4,280 MW). This is the ClimateFEAT baseline.

- **High (6,510 MW):** 2025 IEPR Final High case, adopted January 2026. Reflects PG&E's massive application queue explosion (roughly 4,000 MW in large load applications). Source: CEC 2025 IEPR Preliminary Data Center Forecast, October 2025. https://www.energy.ca.gov/sites/default/files/2025-11/2025_IEPR_Preliminary_Data_Center_Forecast_ada.pdf

### CEC Confidence Tiers

The CEC categorizes datacenter applications by development stage and assigns confidence weights:

| Application Stage | Description | Low | Mid | High |
|---|---|---|---|---|
| T&D Planning | Engineering done, actively being built | 100% | 100% | 100% |
| Group 1 | Formal application, engineering underway | 50% | 70% | 70% |
| Group 2 | Application filed, no engineering yet | 0% | 50% | 50% |
| Group 3 | Inquiry without formal application | 0% | 0% | 10% |

A 67% utilization factor converts requested capacity to estimated peak load, based on Silicon Valley Power's analysis of 60+ existing data centers.

### TAC Allocation

DC load is distributed by TAC area based on the ClimateFEAT 2024 baseline: PGE 84.2%, SCE 14.8%, SDGE 1.0%. Nearly 63% of projected load growth by 2040 is in PGE territory.

### Scaling Method

Four DC features are scaled uniformly: cuml_count, cuml_sq_foot, cuml_utility_cap, cuml_dc_load. For each TAC area, the scale factor ramps linearly from 1.0× at 2023 to (target_MW × TAC_share / current_MW) at 2040.

---

## BEV Scaling

### Source Data

Historical BEV registrations from CEC ZEV registrations data:

| Year | Statewide BEV | Annual Increase |
|---|---|---|
| 2018 | 194,156 | — |
| 2019 | 267,512 | +73,356 |
| 2020 | 336,102 | +68,590 |
| 2021 | 442,874 | +106,772 |
| 2022 | 639,348 | +196,474 |
| 2023 | 934,139 | +294,791 |

Average annual increase 2018–2023: approximately 148,000 BEVs per year.

### BEV Trajectories

- **High (100%):** Current ClimateFEAT pipeline projection following the ZEV mandate exponential trajectory. Reaches approximately 12.6 million BEVs statewide by 2040. This is the baseline.

- **Low (50%):** Half the pipeline projection. Reaches approximately 6.3 million BEVs by 2040. Represents a scenario where EV adoption decelerates significantly.

- **Linear (27%):** Historical average annual increase (148,000 BEVs/year) projected forward from 2023. Reaches approximately 3.45 million BEVs by 2040. Represents a scenario where the exponential adoption curve flattens to constant annual additions — for example, if federal EV tax credits are removed and adoption plateaus.

### Extrapolation Context

Training data covers BEV from 194,000 (2018) to 934,000 (2023). All 2040 projections exceed the training maximum:

| Trajectory | 2040 BEV | × Training Max |
|---|---|---|
| High (100%) | 12.6M | 13.5× |
| Low (50%) | 6.3M | 6.7× |
| Linear (27%) | 3.45M | 3.7× |

Per Beucler et al. (2024) "Climate-Invariant Machine Learning" (Science Advances), neural networks have no guarantee of generalizing well far outside their training sets, and different training approaches can lead to drastically different out-of-distribution predictions. The BEV feature is the most extrapolated input in ClimateFEAT's inference pipeline. A sqrt(BEV) transform reduces the extrapolation factor to 3.7× for the High case, matching the weather feature extrapolation range.

### Scaling Method

BEV is scaled uniformly across all counties (not TAC-specific). The scale factor ramps linearly from 1.0× at 2023 to the target fraction at 2040.

---

## Scenario Definitions

| ID | DC Target | BEV Target | Label | Purpose |
|---|---|---|---|---|
| S1 | Mid (4,123 MW) | High (100%) | DC Mid / BEV High | Baseline — full pipeline projections |
| S2 | High (6,510 MW) | High (100%) | DC High / BEV High | Worst case — maximum infrastructure growth |
| S3 | Low (3,644 MW) | Low (50%) | DC Low / BEV Low | Best case — minimum infrastructure growth |
| S4 | High (6,510 MW) | Low (50%) | DC High / BEV Low | AI boom, slow EV — data centers surge, EVs stall |
| S5 | Low (3,644 MW) | High (100%) | DC Low / BEV High | DC stalls, EV mandate — data center growth slows, EV mandate holds |
| S6 | Low (3,644 MW) | Linear (27%) | DC Low / BEV Linear | Weather signal isolator — minimal infrastructure, isolates climate-driven demand |

---

## Key Results (2040, SSP3-7.0, Top-1% Ensemble Mean)

| Scenario | 2040 Peak (MWh) | Growth vs 2025 |
|---|---|---|
| S5: DC Low / BEV High | 77,058 | +22.3% |
| S1: DC Mid / BEV High (baseline) | 77,005 | +22.2% |
| S2: DC High / BEV High | 76,838 | +21.9% |
| S3: DC Low / BEV Low | 75,092 | +19.5% |
| S4: DC High / BEV Low | 74,768 | +18.9% |
| S6: DC Low / BEV Linear | 73,189 | +16.6% |

---

## Demand Decomposition

Comparing scenarios isolates individual driver contributions:

| Comparison | What It Measures | 2040 Effect |
|---|---|---|
| S6 alone | Weather/climate signal with minimal infrastructure | +16.6% |
| S1 minus S6 | BEV acceleration effect (exponential vs linear adoption) | +5.6% |
| S1 minus S5 | DC growth effect (Mid vs Low DC, same BEV) | -0.1% (negligible) |
| S2 minus S1 | DC High vs DC Mid effect | -0.2% (slightly negative — extrapolation artifact) |
| SSP3-7.0 minus SSP2-4.5 | Climate scenario divergence | ~0.5% |
| Ensemble p10 to p90 | Weather model uncertainty | ~7% spread |

### Summary Attribution

| Driver | 2040 Contribution | Share of Growth | Confidence |
|---|---|---|---|
| Weather/climate | +16.6% | ~75% | High — weather features are within distribution |
| BEV acceleration | +5.6% | ~25% | Medium — real direction, extrapolated magnitude |
| Data center growth | <0.3% | ~1% | Low — inconsistent direction across counties |
| SSP scenario choice | ~0.5% | ~2% | Scenarios have not diverged by 2040 |

### BEV Effect by County

The BEV contribution (S1 minus S6) is concentrated in high-adoption urban counties:

| County | S1 - S6 (MWh) |
|---|---|
| Los Angeles | +748 |
| San Diego | +343 |
| Orange | +336 |
| Riverside | +300 |
| San Bernardino | +276 |
| Alameda | +221 |
| Sacramento | +182 |

47 of 57 counties show S1 slightly lower than S6 (negative deltas of -2 to -5 MWh), but urban counties dominate the statewide total.

### DC Effect

Data centers do not meaningfully affect peak demand because they operate as flat 24/7 baseload — they add energy (GWh) but not peak (MW/MWh). The DC High scenario (S2) produces slightly lower predictions than DC Mid (S1), likely due to transformer extrapolation artifacts at 1.58× the training range for DC features. Santa Clara County (largest DC concentration) shows +0.87% at 2030 but -1.07% at 2040, consistent with extrapolation breakdown at extreme feature values.

---

## Implications for Grid Planning

Three-quarters of projected peak demand growth through 2040 is driven by warming temperatures, not infrastructure expansion. This means:

1. Grid capacity investment for peak demand is largely scenario-independent through 2040 — planners do not need to wait for resolution of EV adoption or data center growth uncertainties before acting on transmission and generation buildout.

2. The SSP3-7.0 and SSP2-4.5 pathways produce nearly identical peak demand through 2040 (within 0.5%). Climate scenarios do not meaningfully diverge until after 2040 for electricity demand planning purposes.

3. EV adoption trajectory is the largest infrastructure uncertainty for peak demand, but its effect is concentrated in a small number of urban counties. County-level planning in LA, San Diego, Orange, and the Bay Area should account for EV charging load; rural counties can deprioritize this factor.

4. Data center growth, despite being the largest driver of total energy consumption growth, does not drive peak demand because data centers operate at constant baseload. CEC's treatment of DC load as an additive block is appropriate for energy forecasting but does not affect peak capacity planning.
