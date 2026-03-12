# California Energy Storage

## Overview

Energy storage capacity data from the CEC Energy Storage System Survey, October 2025. Battery storage is critical context for ClimateFEAT demand projections because it serves as dispatchable capacity during peak hours (hour 17–18 summer evenings) when solar output is declining.

- **Total installations**: 284,907
- **Total capacity**: 25,580 MW (25.6 GW)
- **Dominant technology**: Lithium ion (typically 4-hour duration)
- **Data source**: CEC Energy Storage System Survey
- **Data vintage**: October 2025
- **URL**: https://www.energy.ca.gov/data-reports/energy-almanac/california-electricity-data/california-energy-storage-system-survey

## Capacity by Customer Sector

| Sector | Installations | Capacity (MW) | Share |
|--------|-------------:|-------------:|------:|
| Utility | 350 | 22,518 | 88.0% |
| Residential | 280,423 | 2,213 | 8.6% |
| Commercial | 3,797 | 849 | 3.3% |

## Storage Growth Trajectory

| Year | Added (MW) | Cumulative (MW) | Cumulative (GW) | YoY Growth |
|------|----------:|----------------:|----------------:|-----------:|
| 2018 | 218 | 657 | 0.7 | 50% |
| 2019 | 189 | 846 | 0.8 | 29% |
| 2020 | 577 | 1,423 | 1.4 | 68% |
| 2021 | 2,398 | 3,821 | 3.8 | 169% |
| 2022 | 3,122 | 6,944 | 6.9 | 82% |
| 2023 | 2,933 | 9,877 | 9.9 | 42% |
| 2024 | 5,103 | 14,980 | 15.0 | 52% |
| 2025 | 8,152 | 23,132 | 23.1 | 54% |
| 2026 | 2,312 | 25,444 | 25.4 | 10% |
| 2027 | 65 | 25,509 | 25.5 | 0% |
| 2028 | 71 | 25,580 | 25.6 | 0% |

California added 5,103 MW in 2024 and 8,152 MW in 2025, representing explosive growth driven by ITC incentives, declining lithium ion costs, and CPUC procurement mandates.

## Storage by Utility

| Utility | Installations | Capacity (MW) |
|---------|-------------:|-------------:|
| SCE | 99,819 | 13,814 |
| PGAE | 134,233 | 6,227 |
| SDGE | 34,272 | 4,494 |
| IID | 4 | 410 |
| SMUD | 2,427 | 238 |
| VEA | 3 | 150 |
| LADWP | 11,264 | 126 |
| Arizona Public Service | 1 | 89 |
| Modesto Irrigation District | 697 | 7 |
| Anza Electric Co-Op | 2 | 4 |

## Storage by CAISO TAC Area

| TAC Area | Storage (MW) |
|----------|-----------:|
| SCE | 13,009 |
| PGE | 5,481 |
| SDGE | 3,797 |
| **CAISO Total** | **22,287** |

## Storage by County (Top 20)

| Rank | County | Installations | Capacity (MW) |
|------|--------|-------------:|-------------:|
| 1 | Kern | 9,171 | 4,585 |
| 2 | Riverside | 22,788 | 3,336 |
| 3 | San Diego | 30,969 | 1,937 |
| 4 | San Bernardino | 18,126 | 1,507 |
| 5 | Los Angeles | 39,256 | 1,259 |
| 6 | Imperial | 10 | 970 |
| 7 | Orange | 17,366 | 943 |
| 8 | Monterey | 2,587 | 848 |
| 9 | Yuma | 5 | 848 |
| 10 | Kings | 1,442 | 724 |
| 11 | San Joaquin | 6,454 | 646 |
| 12 | Fresno | 8,776 | 575 |
| 13 | La Paz | 4 | 539 |
| 14 | Clark | 5 | 530 |
| 15 | Alameda | 12,461 | 466 |
| 16 | Tulare | 4,482 | 459 |
| 17 | Ventura | 8,356 | 376 |
| 18 | San Mateo | 7,365 | 332 |
| 19 | Contra Costa | 13,984 | 323 |
| 20 | Esmeralda | 3 | 279 |

## Storage by CAISO Interconnection Type

| Category | Installations | Capacity (MW) |
|----------|-------------:|-------------:|
| CAISO BESS | 176 | 11,240 |
| PLANNED CAISO | 89 | 7,084 |
| OTHER | 284,258 | 3,499 |
| CAISO Hybrid | 34 | 2,202 |
| CAISO-OOS BESS | 10 | 924 |
| CAISO-OOS Hybrid | 3 | 630 |

CAISO BESS and CAISO Hybrid represent utility-scale grid-connected storage. PLANNED CAISO entries are approved but not yet operational. OTHER includes behind-the-meter residential and commercial installations.

## Storage Duration and Peak Hour Contribution

Most California battery storage is 4-hour lithium ion. At peak hour (hour 17–18 summer evening), storage can discharge at full nameplate capacity. However, if extreme heat persists for multiple days, storage may not fully recharge from solar the next day (reduced output under extreme heat, increased overnight cooling load).

At 22,287 MW CAISO storage capacity with 4-hour duration, total energy available is approximately 89 GWh per cycle. This is sufficient for a typical 4-hour evening peak but may be inadequate during multi-day heat waves — exactly the scenario ClimateFEAT is designed to project.

## Capacity Adequacy Context

Combined with firm generation (gas, hydro, nuclear, geothermal, bioenergy) from the GEM March 2026 dataset:

| Resource | CAISO Capacity (MW) |
|----------|---------:|
| Firm generation | 49,754 |
| Battery storage | 22,287 |
| **Firm + Storage** | **72,041** |
| Typical peak imports | ~5,000–10,000 |

For comparison, ClimateFEAT projects CAISO peak demand reaching ~71,086 MW by 2040 under SSP3-7.0 (ensemble mean). The CEC's 2025 IEPR projects 66,318 MW (Planning + Known Loads) to 72,099 MW (Local Reliability) by 2040.

## Source

California Energy Commission, Energy Storage System Survey, October 2025. https://www.energy.ca.gov/data-reports/energy-almanac/california-electricity-data/california-energy-storage-system-survey