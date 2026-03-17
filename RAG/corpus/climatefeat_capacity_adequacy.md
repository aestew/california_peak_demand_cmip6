# California Capacity Adequacy Analysis

## Overview

Comparison of existing generation capacity plus energy storage against projected peak demand. Combines GEM March 2026 generation data with CEC Energy Storage Survey (October 2025), CEC 2025 IEPR peak demand projections, and ClimateFEAT transformer ensemble projections under SSP3-7.0 and SSP2-4.5.

**Key distinction**: This analysis models the peak hour (hour 17–18 summer evening). Solar contributes minimally at this hour. Wind is variable. Battery storage (primarily 4-hour lithium ion) can discharge during peak hours and is counted as dispatchable capacity for this analysis.

## Energy Storage in California

Source: CEC Energy Storage System Survey, October 2025.

- **Total installations**: 284,907
- **Total capacity**: 25,580 MW (25.6 GW)
- **Utility-scale (≥1 MW)**: 480 installations, 22,786 MW
- **Distributed (<1 MW)**: 284,090 installations, 2,794 MW
- **Dominant technology**: Lithium ion battery

### Storage Growth Trajectory

| Year | Added (MW) | Cumulative (MW) | Cumulative (GW) |
|------|----------:|----------------:|----------------:|
| 2018 | 218 | 657 | 0.7 |
| 2019 | 189 | 846 | 0.8 |
| 2020 | 577 | 1,423 | 1.4 |
| 2021 | 2,398 | 3,821 | 3.8 |
| 2022 | 3,122 | 6,944 | 6.9 |
| 2023 | 2,933 | 9,877 | 9.9 |
| 2024 | 5,103 | 14,980 | 15.0 |
| 2025 | 8,152 | 23,132 | 23.1 |
| 2026 | 2,312 | 25,444 | 25.4 |
| 2027 | 65 | 25,509 | 25.5 |
| 2028 | 71 | 25,580 | 25.6 |

### Storage by Utility / TAC Area (through 2025)

| TAC Area | Storage MW |
|----------|----------:|
| SCE | 13,009 |
| PGE | 5,481 |
| SDGE | 3,797 |
| **CAISO Total** | **22,287** |

### Storage by County (top 15)

| County | Storage MW |
|--------|-----------:|
| Kern | 4,585 |
| Riverside | 3,336 |
| San Diego | 1,937 |
| San Bernardino | 1,507 |
| Los Angeles | 1,259 |
| Imperial | 970 |
| Orange | 943 |
| Monterey | 848 |
| Yuma | 848 |
| Kings | 724 |
| San Joaquin | 646 |
| Fresno | 575 |
| La Paz | 539 |
| Clark | 530 |
| Alameda | 466 |

## Combined Capacity Adequacy: Generation + Storage


### CAISO Total

- **Firm generation**: 49,754 MW
- **Variable generation (solar + wind)**: 27,606 MW
- **Battery storage**: 22,287 MW
- **Firm + Storage (peak-hour dispatchable)**: 72,041 MW

| Year | CEC Planning (MW) | CEC Local Rel. (MW) | ClimateFEAT SSP3-7.0 (MW) | Firm Gen (MW) | + Storage (MW) | Margin (CEC Plan.) | Margin (ClimateFEAT) | Margin (Local Rel.) |
|------|------------------:|--------------------:|--------------------------:|--------------:|---------------:|-------------------:|---------------------:|--------------------:|
| 2025 | 46,487 | 46,487 | 57,491 | 49,754 | 72,041 | +25,554 | +14,550 | +25,554 |
| 2030 | 55,843 | 58,361 | 61,926 | 49,754 | 72,041 | +16,198 | +10,115 | +13,680 |
| 2035 | 61,898 | 67,672 | 66,288 | 49,754 | 72,041 | +10,143 | +5,753 | +4,369 |
| 2040 | 66,318 | 72,099 | 69,965 | 49,754 | 72,041 | +5,723 | +2,076 | -58 |

### PG&E TAC

- **Firm generation**: 29,118 MW
- **Variable generation (solar + wind)**: 12,675 MW
- **Battery storage**: 5,481 MW
- **Firm + Storage (peak-hour dispatchable)**: 34,599 MW

| Year | CEC Planning (MW) | ClimateFEAT (MW) | Firm Gen (MW) | + Storage (MW) | Margin (CEC) | Margin (CF) | Status |
|------|------------------:|-----------------:|--------------:|---------------:|-------------:|------------:|--------|
| 2025 | 20,718 | 23,081 | 29,118 | 34,599 | +13,881 | +11,518 | ✅ Surplus |
| 2030 | 26,599 | 24,220 | 29,118 | 34,599 | +8,000 | +10,379 | ✅ Surplus |
| 2035 | 30,180 | 26,135 | 29,118 | 34,599 | +4,419 | +8,464 | ✅ Surplus |
| 2040 | 32,437 | 27,816 | 29,118 | 34,599 | +2,162 | +6,783 | ✅ Surplus |

### SCE TAC

- **Firm generation**: 17,673 MW
- **Variable generation (solar + wind)**: 14,572 MW
- **Battery storage**: 13,009 MW
- **Firm + Storage (peak-hour dispatchable)**: 30,682 MW

| Year | CEC Planning (MW) | ClimateFEAT (MW) | Firm Gen (MW) | + Storage (MW) | Margin (CEC) | Margin (CF) | Status (CF) |
|------|------------------:|-----------------:|--------------:|---------------:|-------------:|------------:|-------------|
| 2025 | 23,617 | 29,180 | 17,673 | 30,682 | +7,065 | +1,502 | ✅ Surplus |
| 2030 | 26,573 | 31,908 | 17,673 | 30,682 | +4,109 | -1,226 | ⚠️ DEFICIT |
| 2035 | 28,453 | 33,984 | 17,673 | 30,682 | +2,229 | -3,302 | ⚠️ DEFICIT |
| 2040 | 30,277 | 35,681 | 17,673 | 30,682 | +405 | -4,999 | ⚠️ DEFICIT |

**Note**: ClimateFEAT projects significantly higher SCE TAC demand than CEC, driven by stronger climate signal in inland Southern California counties (Riverside, San Bernardino, Kern). Under ClimateFEAT projections, SCE enters firm+storage deficit by **~2029**.

### SDG&E TAC

- **Firm generation**: 2,963 MW
- **Variable generation (solar + wind)**: 358 MW
- **Battery storage**: 3,797 MW
- **Firm + Storage (peak-hour dispatchable)**: 6,760 MW

| Year | CEC Planning (MW) | ClimateFEAT (MW) | Firm Gen (MW) | + Storage (MW) | Margin (CEC) | Margin (CF) | Status (CF) |
|------|------------------:|-----------------:|--------------:|---------------:|-------------:|------------:|-------------|
| 2025 | 4,236 | 5,230 | 2,963 | 6,760 | +2,524 | +1,530 | ✅ Surplus |
| 2030 | 4,679 | 5,797 | 2,963 | 6,760 | +2,081 | +963 | ✅ Surplus |
| 2035 | 5,034 | 6,169 | 2,963 | 6,760 | +1,726 | +591 | ✅ Surplus |
| 2040 | 5,438 | 6,468 | 2,963 | 6,760 | +1,322 | +292 | ✅ Surplus |

## The Big Picture: When Does California Run Out?

Three views of CAISO capacity adequacy at peak hour:

| Resource | Capacity (MW) |
|----------|--------------:|
| Firm generation (gas, hydro, nuclear, geo, bio) | 49,754 |
| Battery storage (through 2025) | 22,287 |
| **Firm + Storage** | **72,041** |
| Imports (typical peak) | ~5,000–10,000 |
| **Total available at peak (conservative est.)** | **~77,041–82,041** |

| Year | CEC Planning (MW) | CEC Local Rel. (MW) | ClimateFEAT SSP3-7.0 (MW) | Firm+Storage | Margin (Planning) | Margin (ClimateFEAT) | Margin (Local Rel.) |
|------|------------------:|--------------------:|--------------------------:|-------------:|------------------:|---------------------:|--------------------:|
| 2025 | 46,487 | 46,487 | 57,491 | 72,041 | +25,554 | +14,550 | +25,554 |
| 2030 | 55,843 | 58,361 | 61,926 | 72,041 | +16,198 | +10,115 | +13,680 |
| 2035 | 61,898 | 67,672 | 66,288 | 72,041 | +10,143 | +5,753 | +4,369 |
| 2040 | 66,318 | 72,099 | 69,965 | 72,041 | +5,723 | +2,076 | -58 |

ClimateFEAT SSP3-7.0 ensemble range at 2040: 67,539–72,675 MW (10th–90th percentile). Under the 90th percentile projection, firm+storage enters deficit by ~2037.

### Key Findings

- **CEC Planning scenario**: Firm+Storage sufficient through 2040 (2040 margin: +5,723 MW)
- **ClimateFEAT SSP3-7.0**: Firm+Storage margin at 2040: +2,076 MW mean, **deficit under 90th percentile ensemble members**
- **CEC Local Reliability**: Firm+Storage deficit begins by **2040** (-58 MW)
- **With imports (~7,500 MW avg)**: Total available ~79,541 MW — sufficient under all scenarios through 2040
- **Without imports or storage growth**: Firm generation alone (49,754 MW) enters deficit by **2028** under ClimateFEAT projections

### Critical Caveat: Storage Duration

Most California battery storage is 4-hour duration. At 22,287 MW for 4 hours, total energy is ~89 GWh. If peak demand persists for longer than 4 hours (e.g., multi-day heat waves), storage depletes and only firm generation + imports remain. This is exactly the scenario ClimateFEAT is designed to project — sustained multi-day heat events where rolling temperature aggregates drive compounding demand.

### Storage Growth Matters

California added 5,103 MW of storage in 2024 alone and 8,152 MW in 2025. If this pace continues (~5–8 GW/year), storage could add 25–40 GW by 2030, substantially changing the adequacy picture. However, this growth rate depends on ITC incentives, supply chain capacity, interconnection queue processing, and grid upgrade timelines.

## Sources

- Generation: Global Energy Monitor, Global Integrated Power Tracker, March 2026
- Storage: CEC Energy Storage System Survey, October 2025
- CEC Demand: CEC 2025 IEPR (TN 267942, Fugate presentation, December 2025)
- ClimateFEAT Demand: ClimateFEAT transformer ensemble projections (7 CMIP6 models, SSP3-7.0 and SSP2-4.5)
- CEC storage survey: https://www.energy.ca.gov/data-reports/energy-almanac/california-electricity-data/california-energy-storage-system-survey