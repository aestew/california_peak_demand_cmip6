# ClimateFEAT vs CEC Peak Demand Comparison

## Overview

Direct comparison of ClimateFEAT projected peak demand against the CEC's 2025 IEPR forecast (adopted January 21, 2026). Both use peak hourly load in MW. ClimateFEAT values are the ensemble mean of top-1% peak days per year. CEC values are 1-in-2 coincident peak from the Fugate presentation (TN 267942, December 17, 2025).

**Key methodological differences:**

- CEC uses econometric sector models + WRF weather variants (4 detrended runs, SSP3-7.0 only)
- ClimateFEAT uses a multi-stream transformer + CMIP6 ensembles (24 runs SSP3-7.0, 24 runs SSP2-4.5, trend retained)
- CEC includes load modifiers (AAEE, AAFS, AATE, known loads) as additive adjustments
- ClimateFEAT includes data center and EV features as model inputs but does not add separate load modifier scenarios
- CEC forecasts at planning area level; ClimateFEAT forecasts at county level, rolled up via population-weighted TAC allocation


## CAISO Total — SSP3-7.0 vs CEC

| Year | ClimateFEAT Mean (MW) | ClimateFEAT 10th | ClimateFEAT 90th | CEC Planning | CEC Planning + Known Loads | CEC Local Reliability |
|------|----------------------:|-----------------:|-----------------:|-------------:|---------------------------:|----------------------:|
| 2025 | 56,033 | 53,707 | 58,806 | 46,487 | 46,487 | 46,487 |
| 2030 | 61,267 | 60,130 | 62,848 | 51,062 | 55,843 | 58,361 |
| 2035 | 66,471 | 64,412 | 69,804 | 57,370 | 61,898 | 67,672 |
| 2040 | 71,086 | 67,843 | 74,221 | 61,790 | 66,318 | 72,099 |

ClimateFEAT growth 2025→2040: +26.9%
CEC Planning growth 2025→2040: +32.9%
CEC Local Reliability growth 2025→2040: +55.1%

## CAISO Total — SSP2-4.5 vs CEC

| Year | ClimateFEAT Mean (MW) | ClimateFEAT 10th | ClimateFEAT 90th | CEC Planning | CEC Planning + Known Loads | CEC Local Reliability |
|------|----------------------:|-----------------:|-----------------:|-------------:|---------------------------:|----------------------:|
| 2025 | 56,042 | 53,892 | 58,611 | 46,487 | 46,487 | 46,487 |
| 2030 | 61,905 | 60,215 | 63,732 | 51,062 | 55,843 | 58,361 |
| 2035 | 66,388 | 64,036 | 69,026 | 57,370 | 61,898 | 67,672 |
| 2040 | 70,868 | 68,198 | 74,413 | 61,790 | 66,318 | 72,099 |

ClimateFEAT growth 2025→2040: +26.5%
CEC Planning growth 2025→2040: +32.9%
CEC Local Reliability growth 2025→2040: +55.1%

## TAC-Level Comparison — SSP3-7.0 vs CEC

CEC non-coincident peak by planning area vs ClimateFEAT TAC-allocated peak.


### PG&E TAC

| Year | ClimateFEAT Mean (MW) | 10th Pct | 90th Pct | CEC Planning | CEC + Known Loads |
|------|----------------------:|--------:|---------:|-------------:|------------------:|
| 2025 | 23,414 | 22,580 | 24,498 | 20,718 | 20,718 |
| 2030 | 24,541 | 23,346 | 25,390 | 23,817 | 26,599 |
| 2035 | 26,675 | 25,749 | 27,670 | 27,399 | 30,180 |
| 2040 | 28,772 | 27,671 | 30,254 | 29,656 | 32,437 |

ClimateFEAT growth 2025→2040: +22.9%
CEC Planning growth 2025→2040: +43.1%

### SCE TAC

| Year | ClimateFEAT Mean (MW) | 10th Pct | 90th Pct | CEC Planning | CEC + Known Loads |
|------|----------------------:|--------:|---------:|-------------:|------------------:|
| 2025 | 28,629 | 27,445 | 29,995 | 23,617 | 23,617 |
| 2030 | 31,987 | 31,211 | 32,997 | 24,509 | 26,573 |
| 2035 | 34,731 | 33,273 | 36,153 | 26,389 | 28,453 |
| 2040 | 36,719 | 35,152 | 38,768 | 28,213 | 30,277 |

ClimateFEAT growth 2025→2040: +28.3%
CEC Planning growth 2025→2040: +19.5%

### SDG&E TAC

| Year | ClimateFEAT Mean (MW) | 10th Pct | 90th Pct | CEC Planning | CEC + Known Loads |
|------|----------------------:|--------:|---------:|-------------:|------------------:|
| 2025 | 5,004 | 4,814 | 5,200 | 4,236 | 4,236 |
| 2030 | 5,905 | 5,806 | 6,070 | 4,503 | 4,679 |
| 2035 | 6,420 | 6,238 | 6,635 | 4,858 | 5,034 |
| 2040 | 6,792 | 6,605 | 7,050 | 5,318 | 5,438 |

ClimateFEAT growth 2025→2040: +35.7%
CEC Planning growth 2025→2040: +25.5%

## Interpretation Notes

- ClimateFEAT values are top-1% peak day ensemble means; CEC values are 1-in-2 weather year peaks. These are conceptually similar but not identical.
- CEC includes additive load modifiers (transportation electrification, fuel substitution, efficiency) that ClimateFEAT captures differently — as learned features rather than exogenous adjustments.
- Where ClimateFEAT exceeds CEC projections, this may reflect the climate signal captured by trend-retained CMIP6 projections that the CEC's detrended WRF approach misses.
- Where CEC exceeds ClimateFEAT, this likely reflects load modifiers (especially known loads and transportation electrification) that are modeled as additive blocks in the CEC framework.
- The ClimateFEAT ensemble spread (10th–90th percentile) provides uncertainty bounds that the CEC does not produce for climate-driven demand variation.

## Sources

- CEC: Nick Fugate, Draft CED 2025 Hourly & Peak Forecast (TN 267942, December 17, 2025)
- ClimateFEAT: Transformer inference across CMIP6 LOCA2-Hybrid ensemble
- Generated: March 2026