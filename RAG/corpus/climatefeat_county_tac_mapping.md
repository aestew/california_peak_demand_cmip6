# ClimateFEAT County-to-TAC Mapping

## Overview

ClimateFEAT produces county-level forecasts for all 58 California counties. To compare against CEC planning area forecasts and CAISO TAC (Transmission Access Charge) area aggregations, county-level predictions must be rolled up to TAC areas. Most counties map cleanly to a single TAC area. Approximately 12 counties are split between two service territories, requiring population-weighted allocation.

## TAC Areas

CAISO operates three IOU TAC areas corresponding to the three investor-owned utilities:

- **PG&E TAC**: Northern and Central California
- **SCE TAC**: Southern California (inland and coastal)
- **SDG&E TAC**: San Diego region

Non-CAISO service territories (not included in CAISO TAC aggregations):

- **LADWP**: City of Los Angeles and surrounding areas
- **SMUD**: Sacramento Municipal Utility District
- **IID**: Imperial Irrigation District
- **VEA**: Valley Electric Association (small area in Inyo County)
- **Other munis**: Burbank, Glendale, Pasadena, Silicon Valley Power, etc.

## County-to-TAC Assignment

### PG&E TAC — Sole Territory (30 counties)

Alameda, Alpine, Amador, Butte, Calaveras, Colusa, Contra Costa, El Dorado, Glenn, Humboldt, Lake, Lassen, Marin, Mendocino, Merced, Modoc, Monterey, Napa, Nevada, Placer, Plumas, San Benito, San Francisco, San Joaquin, San Luis Obispo, San Mateo, Santa Clara, Santa Cruz, Shasta, Sierra, Siskiyou, Solano, Sonoma, Stanislaus, Sutter, Tehama, Trinity, Yolo, Yuba

### SCE TAC — Sole Territory (4 counties)

Orange, Riverside, San Bernardino, Ventura

### SDG&E TAC — Sole Territory (1 county)

San Diego

### Split Counties — PG&E / SCE

These counties straddle the PG&E and SCE service territory boundary. Population-weighted split percentages are approximate, based on CEC planning area definitions and population distribution.

| County | PG&E Share | SCE Share | Notes |
|--------|-----------|-----------|-------|
| Kern | 55% | 45% | Bakersfield area is PG&E; Tehachapi and south Kern are SCE |
| Santa Barbara | 60% | 40% | North coast (Santa Maria) is PG&E; south (Santa Barbara city) is SCE |
| Tulare | 40% | 60% | Visalia and Porterville are SCE territory |
| Kings | 70% | 30% | Hanford area split; majority PG&E |
| Fresno | 95% | 5% | Small southern slice is SCE |
| Madera | 95% | 5% | Small southern slice is SCE |
| Tuolumne | 95% | 5% | Small eastern portion is SCE |

### Split Counties — SCE / Non-CAISO

These counties are partially served by municipal utilities outside CAISO.

| County | SCE Share | Non-CAISO Entity | Non-CAISO Share | Notes |
|--------|-----------|-------------------|-----------------|-------|
| Los Angeles | 70% | LADWP | 30% | City of LA served by LADWP; rest is SCE |
| Imperial | 10% | IID | 90% | Mostly Imperial Irrigation District |
| Mono | 90% | LADWP | 10% | Small LADWP presence |
| Inyo | 80% | LADWP / VEA | 20% | LADWP serves Owens Valley; VEA serves small area |

### Split Counties — PG&E / Non-CAISO

| County | PG&E Share | Non-CAISO Entity | Non-CAISO Share | Notes |
|--------|-----------|-------------------|-----------------|-------|
| Sacramento | 55% | SMUD | 45% | City of Sacramento and surrounding served by SMUD |

## How to Use for TAC Rollups

To aggregate county-level predictions to TAC areas:

1. For sole-territory counties: assign 100% of the county prediction to the TAC area
2. For split counties: multiply the county prediction by the population share percentage for each TAC area
3. Sum across all contributing counties for each TAC area

Example for Kern County with predicted peak of 1,000 MWh:
- PG&E TAC contribution: 1,000 × 0.55 = 550 MWh
- SCE TAC contribution: 1,000 × 0.45 = 450 MWh

## Limitations

- Split percentages are approximate and based on population distribution, not metered load
- Municipal utility territories (LADWP, SMUD, IID) are excluded from CAISO TAC totals but ClimateFEAT still produces forecasts for those counties
- Actual load splits may differ from population splits due to differences in commercial/industrial concentration
- Some small municipal utilities within IOU territories (Burbank, Glendale, Pasadena, Silicon Valley Power, Roseville) are not broken out at the county level

## CEC Planning Area to TAC Crosswalk

The CEC forecasts by 8 planning areas. The mapping to TAC areas:

| CEC Planning Area | Primary TAC | Notes |
|-------------------|-------------|-------|
| PG&E | PG&E TAC | Includes PG&E share of split counties |
| SCE | SCE TAC | Includes SCE share of split counties |
| SDG&E | SDG&E TAC | San Diego County |
| LADWP | Non-CAISO | City of LA + portions of Inyo, Mono |
| SMUD | Non-CAISO | Sacramento area |
| IID | Non-CAISO | Imperial County |
| NCNC (Northern CA Non-CAISO) | Non-CAISO | Small munis in Northern CA |
| Burbank/Glendale | Non-CAISO | Los Angeles County munis |

## Source

County assignments based on CEC Electric Load Serving Entities GIS data (https://cecgis-caenergy.opendata.arcgis.com/datasets/CAEnergy::electric-load-serving-entities-iou-pou) and SCE service territory documentation (updated March 2025). Population split percentages are estimates based on CEC planning area definitions and 2020 Census population distribution.