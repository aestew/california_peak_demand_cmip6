# California Peak Electricity Demand Forecasting with CMIP6 Climate Projections

County-level peak demand forecasting through 2040 using CMIP6 climate ensembles and a custom PyTorch transformer.

## Problem

The CEC's current demand forecasting relies on 33 weather stations, CAISO-only load data (~80% of the state), limited climate scenario coverage, and econometric regression. This project replaces that approach with ML models trained on high-resolution gridded climate data across multiple emission scenarios.


## Model

**ClimateFEAT** is a custom multi-stream transformer with four feature streams (climate, temporal, demographic, infrastructure) and two-phase attention — within-stream self-attention followed by cross-stream fusion. Inference runs across 7 CMIP6 models under SSP2-4.5 (25 ensembles) and SSP3-7.0 (15 ensembles).

## Data

- **Climate historicals:** URMA 2.5km gridded observations (GRIB2 → Zarr)
- **Climate projections:** CMIP6 ensemble output (ACCESS-CM2, EC-Earth3, EC-Earth3-Veg, GFDL-ESM4, INM-CM5-0, MPI-ESM1-2-HR, MRI-ESM2-0)
- **Population:** WorldPop 1km regridded to URMA via nearest-neighbor spatial aggregation
- **Load:** CAISO + non-CAISO utility data, county-allocated

## Repo Structure

```
├── pipeline/
│   ├── 00_worldpop_spatial_aggregation.ipynb
│   ├── 01_urma_ingestion.ipynb
│   ├── 02_urma_eda.ipynb
│   ├── 03_urma_align_counties.ipynb
│   ├── 04_urma_feat_eng_population_weight.ipynb
│   ├── 05_build_complete_dataset.ipynb
│   └── inference_data_loca2_processing.ipynb
├── models/
│   ├── lightgbm_peak_demand.ipynb
│   └── climatefeat_transformer.ipynb
└── README.md
```

## Author

**Amy Steward** — UC Berkeley MIDS (2024–2026) 
[LinkedIn](https://linkedin.com/in/amyesteward/) · [Medium](https://medium.com/@aestew) · [GitHub](https://github.com/aestew)

_EV data, Data Center initial dataset, county population, income, and calendar data were added and joined for final models by Kristen Lin and Chad Adelman_

_Work completed by Amy Steward as part of larger capstone project_









