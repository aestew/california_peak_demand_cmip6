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
| 2025 | 56,039 | 54,142 | 58,451 | 46,487 | 46,487 | 46,487 |
| 2030 | 60,430 | 59,506 | 61,641 | 51,062 | 55,843 | 58,361 |
| 2035 | 64,748 | 63,039 | 66,790 | 57,370 | 61,898 | 67,672 |
| 2040 | 68,625 | 66,258 | 71,004 | 61,790 | 66,318 | 72,099 |

ClimateFEAT growth 2025→2040: +22.5%
CEC Planning growth 2025→2040: +32.9%
CEC Local Reliability growth 2025→2040: +55.1%

## CAISO Total — SSP2-4.5 vs CEC

| Year | ClimateFEAT Mean (MW) | ClimateFEAT 10th | ClimateFEAT 90th | CEC Planning | CEC Planning + Known Loads | CEC Local Reliability |
|------|----------------------:|-----------------:|-----------------:|-------------:|---------------------------:|----------------------:|
| 2025 | 55,925 | 53,540 | 58,243 | 46,487 | 46,487 | 46,487 |
| 2030 | 60,798 | 59,049 | 62,416 | 51,062 | 55,843 | 58,361 |
| 2035 | 64,517 | 62,941 | 66,183 | 57,370 | 61,898 | 67,672 |
| 2040 | 68,180 | 65,964 | 71,023 | 61,790 | 66,318 | 72,099 |

ClimateFEAT growth 2025→2040: +21.9%
CEC Planning growth 2025→2040: +32.9%
CEC Local Reliability growth 2025→2040: +55.1%

## TAC-Level Comparison — SSP3-7.0 vs CEC

CEC non-coincident peak by planning area vs ClimateFEAT TAC-allocated peak.


### PG&E TAC

| Year | ClimateFEAT Mean (MW) | 10th Pct | 90th Pct | CEC Planning | CEC + Known Loads |
|------|----------------------:|--------:|---------:|-------------:|------------------:|
| 2025 | 22,951 | 22,390 | 23,798 | 20,718 | 20,718 |
| 2030 | 24,092 | 23,175 | 24,600 | 23,817 | 26,599 |
| 2035 | 26,012 | 25,304 | 26,707 | 27,399 | 30,180 |
| 2040 | 27,683 | 26,761 | 28,814 | 29,656 | 32,437 |

ClimateFEAT growth 2025→2040: +20.6%
CEC Planning growth 2025→2040: +43.1%

### SCE TAC

| Year | ClimateFEAT Mean (MW) | 10th Pct | 90th Pct | CEC Planning | CEC + Known Loads |
|------|----------------------:|--------:|---------:|-------------:|------------------:|
| 2025 | 29,002 | 27,895 | 30,082 | 23,617 | 23,617 |
| 2030 | 31,697 | 30,992 | 32,600 | 24,509 | 26,573 |
| 2035 | 33,775 | 32,726 | 35,217 | 26,389 | 28,453 |
| 2040 | 35,481 | 34,222 | 36,790 | 28,213 | 30,277 |

ClimateFEAT growth 2025→2040: +22.3%
CEC Planning growth 2025→2040: +19.5%

### SDG&E TAC

| Year | ClimateFEAT Mean (MW) | 10th Pct | 90th Pct | CEC Planning | CEC + Known Loads |
|------|----------------------:|--------:|---------:|-------------:|------------------:|
| 2025 | 5,199 | 4,990 | 5,346 | 4,236 | 4,236 |
| 2030 | 5,764 | 5,655 | 5,892 | 4,503 | 4,679 |
| 2035 | 6,131 | 5,985 | 6,312 | 4,858 | 5,034 |
| 2040 | 6,433 | 6,239 | 6,610 | 5,318 | 5,438 |

ClimateFEAT growth 2025→2040: +23.8%
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