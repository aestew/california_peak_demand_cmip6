# ClimateFEAT Data Pipeline Documentation

## Overview

The ClimateFEAT data pipeline transforms raw gridded weather observations and climate projections into county-level, population-weighted daily features suitable for model training and inference. The pipeline is implemented across seven Jupyter notebooks, each handling a distinct stage. Historical training data flows through notebooks 00–05. Future projection data for inference flows through a separate LOCA2 processing notebook that mirrors the same spatial aggregation and feature computation logic.

## Pipeline Architecture

- Stage 0: Population grid construction (00_worldpop_spatial_aggregation)
- Stage 1: URMA weather ingestion from GRIB2 to zarr (01_urma_ingestion)
- Stage 2: URMA exploratory data analysis and QC (02_urma_eda)
- Stage 3: County assignment via TIGER spatial join (03_urma_align_counties)
- Stage 4: Feature engineering and population-weighted aggregation (04_urma_feat_eng_population_weight)
- Stage 5: Merge with non-weather datasets to build complete training set (05_build_complete_dataset)
- Stage 6: LOCA2 CMIP6 processing for inference (inference_data_loca2_processing)

---

## Stage 0: Population Grid (00_worldpop_spatial_aggregation)

### Purpose

Create a population density grid aligned to the URMA weather grid so that climate variables can be population-weighted during spatial aggregation. This is the foundational step that enables the "pop" suffix features throughout the entire pipeline — without it, every weather variable would be a simple area average that treats uninhabited desert and dense urban cores equally.

### Why Population Weighting Matters

California counties vary enormously in size and habitability. San Bernardino County is 20,000+ square miles — most of it empty Mojave Desert — but nearly all its residents live in the western corridor near Fontana and Ontario. A simple area-mean temperature for San Bernardino would be dominated by 120°F desert readings that affect nobody's electricity bill. Population weighting ensures the temperature features reflect conditions where people actually live and consume electricity. The same logic applies to every county with significant uninhabited land: Inyo, Kern, Riverside, Imperial, and most of the rural northern counties.

### Data Source: WorldPop

WorldPop provides global population estimates at 1 km resolution, derived from census data disaggregated using satellite imagery, land cover classification, and settlement pattern modeling. ClimateFEAT uses the R2025A constrained release (USA-specific), which distributes population only into areas identified as built settlements — so wilderness, water, and agricultural land receive zero population. This is better for our use case than unconstrained estimates, which spread population across entire administrative units including unpopulated areas.

Source URL pattern: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{year}/USA/v1/1km_ua/constrained/usa_pop_{year}_CN_1km_R2025A_UA_v1.tif

Years downloaded: 2019–2021. The 2020 baseline year is used for all population weighting to prevent data leakage (population counts don't change by year in the weighting — only the 2020 snapshot is used).

### Processing Steps

Step 1 — Clip to California: The full USA GeoTIFF is "cookie cut" to California's boundary using a Census TIGER 2023 state shapefile (STATEFP 06), converted to EPSG:4326. This is done with rasterio.mask, which zeros out all pixels outside the California polygon. The raw USA file is deleted after clipping to save disk space.

Step 2 — Build spatial index on URMA grid: A KDTree (scipy.spatial.cKDTree) is constructed from the URMA grid cell center coordinates. The URMA grid is approximately 2.5 km resolution with dimensions 535 × 457 (about 245,000 cells covering the California bounding box). The longitude coordinates must be converted from URMA's native 0–360 convention to -180/180 before building the tree.

Step 3 — Nearest-neighbor assignment: Each 1 km WorldPop pixel center is queried against the KDTree to find its nearest URMA cell center. This assigns every WorldPop pixel to exactly one URMA cell. Since the URMA grid (2.5 km) is coarser than WorldPop (1 km), roughly 4–6 WorldPop pixels fall within each URMA cell depending on alignment.

Step 4 — Sum population per URMA cell: All WorldPop pixel populations assigned to the same URMA cell are summed. This produces a single population count per URMA grid cell that represents the total number of people living within that cell's footprint. The result is stored as an xarray DataArray with the same (y, x) dimensions as the URMA grid.

### How the Population Grid Is Used Downstream

In Stage 4 (population-weighted aggregation), the population grid serves as the weighting function. For a given weather variable at a given date, the county-level population-weighted mean is:

weighted_mean = sum(weather_value_i × population_i) / sum(population_i)

where i iterates over all URMA grid cells within the county. A cell in downtown Los Angeles with 50,000 people contributes 1,000× more to LA County's temperature than a cell in the Angeles National Forest with 50 people. This is computed identically for both URMA historical data (Stage 4) and LOCA2 future projections (Stage 6), though the LOCA2 pipeline regrids the population from the URMA grid to the LOCA2 grid using nearest-neighbor interpolation first.

### Assumptions and Limitations

The nearest-neighbor assignment is imperfect at grid cell boundaries — a WorldPop pixel right on the edge between two URMA cells could be assigned to either one depending on which center is fractionally closer. This introduces minor spatial noise but does not systematically bias any county's population count. The total California population from the aggregated grid was validated against Census estimates to confirm reasonable agreement.

Population is held static at 2020 for weighting purposes across all historical years (2018–2025). This is a deliberate choice to prevent the population itself from becoming a confounding variable in the weather features — we want the population weight to reflect where people live, not to introduce a population growth trend into temperature features. Actual population growth enters the model separately through the total_pop feature in the demographic stream.

---

## Stage 1: URMA Ingestion (01_urma_ingestion)

### Purpose

Download raw URMA (Unrestricted Mesoscale Analysis) GRIB2 files from NOAA and consolidate into annual zarr stores.

### Data Source

NOAA URMA via the Herbie Python library, which handles GRIB2 index parsing and variable extraction. URMA provides 2.5 km gridded analysis over CONUS, updated hourly.

### Variables Extracted and Their UTC Analysis Times

- t2m_max_k: Maximum 2m temperature (8 UTC = midnight PT, captures previous day's max)
- t2m_min_k: Minimum 2m temperature (20 UTC = noon PT, captures overnight min)
- dpt_afternoon_k: Afternoon dewpoint at 2m (22 UTC = 2-3 PM PT)
- dpt_morning_k: Morning dewpoint at 2m (14 UTC = 6-7 AM PT)
- cloud_cover_pct: Total cloud cover, entire atmosphere (20 UTC = noon PT, peak solar)
- wind_peak_ms: Peak wind speed at 10m (22 UTC = 2-3 PM PT, peak demand)
- wind_low_ms: Low wind speed at 10m (8 UTC = midnight PT, low demand)
- spfh_peak_kgkg: Specific humidity at 2m (22 UTC = 2-3 PM PT, peak A/C load)

The analysis times were deliberately chosen to align with electricity demand patterns — peak temperature and humidity are captured at afternoon hours when A/C load is highest.

### Spatial Extent and Storage

California bounding box: lat 32.0–42.5, lon -124.5 to -114.0. Data outside this box is dropped before writing to zarr. Each year is processed into a separate zarr store (URMA_RAW_{YEAR}.zarr) with dimensions (date, y, x) where the grid is approximately 535 × 457 cells.

Years processed: 2018–2025 (one zarr per year).

---

## Stage 2: URMA EDA (02_urma_eda)

### Purpose

Quality control and exploratory analysis of raw URMA zarr stores before further processing.

### Checks Performed

Min/max ranges for all variables to catch ingestion errors, null counts per variable, lag-1 day autocorrelation of temperature (confirms physical coherence — tomorrow's temperature is correlated with today's), seasonal climatology verification (groupby dayofyear), spatial plots of annual mean temperature to confirm the geographic pattern looks correct (coastal vs inland gradient), and diurnal temperature range analysis.

This stage produces no output files — it validates that Stage 1 data is clean before passing to Stage 3.

---

## Stage 3: County Assignment (03_urma_align_counties)

### Purpose

Assign each URMA grid cell to a California county so that spatial aggregation can be performed at the county level.

### Process

URMA latitude/longitude coordinates are converted from the grid's native CRS to EPSG:4326. A GeoDataFrame of URMA cell center points is spatially joined (gpd.sjoin, predicate="within") against Census TIGER 2023 county boundaries (FIPS state 06, all 58 California counties). Each grid cell receives a county label; cells outside California are labeled "Outside_CA". The county assignment is stored as a coordinate on the xarray dataset with dimensions (y, x).

### QC Checks

Verification that exactly 58 California counties are found, test point validation for known locations (Sacramento at -121.5/38.5, LA at -118.2/34.1, SF at -122.4/37.8, Fresno at -119.8/36.7), and grid cell counts per county to confirm reasonable spatial distribution.

### Output

Zarr store with county coordinate added (URMA_COUNTY_{YEAR}.zarr).

---

## Stage 4: Feature Engineering and Population Weighting (04_urma_feat_eng_population_weight)

### Purpose

Compute county-level daily weather features in both area-mean and population-weighted variants, plus derived degree day features.

### Area-Mean Aggregation

For each variable, the data is stacked from (date, y, x) to (date, cell), cells are grouped by county coordinate, and the simple mean is computed across all cells in the county. This produces the _mean suffix features.

### Population-Weighted Aggregation

Same stacking, but each cell's value is multiplied by its WorldPop 2020 population before summing within the county group, then divided by the county's total population sum. Formally: weighted_mean = sum(value_i × pop_i) / sum(pop_i) for all cells i in the county. This produces the _pop suffix features. The 2020 population baseline is used for all years to prevent data leakage.

### Degree Day Computation

Average temperature (tavg) is computed at the grid level as (tmax + tmin) / 2 before aggregation. CDD65 = max(tavg - 291.48K, 0), HDD65 = max(291.48K - tavg, 0), CDD75 = max(tavg - 297.04K, 0), where 291.48K = 65°F and 297.04K = 75°F. Degree days are computed on the raw grid first, then population-weighted to county level — this preserves subgrid variability rather than computing degree days from already-aggregated county temperatures.

### Output

24 features per county per day, stored first as zarr then exported to parquet for easier downstream merging.

---

## Stage 5: Complete Dataset Assembly (05_build_complete_dataset)

### Purpose

Merge the weather feature parquets with all non-weather data sources to create the final training dataset.

### Merge Sequence

All left joins on the weather base table, with row count validation via safe_merge to catch many-to-many join errors:

1. Weather features (parquet from Stage 4) — base table with (date, county) as primary key
2. Calendar reference — merged on date. Adds year, month, day_of_week, day_of_year, quarter, holiday, is_holiday
3. Electricity demand — raw hourly data from OEDI (wide format with counties as columns) is melted to long format, timestamps are floored to date and timezone-stripped, then the daily max load (MWh) per county is computed via groupby max. Merged on (date, county)
4. Income — county median income merged on (year, county)
5. Population and housing — DOF demographic estimates merged on (year, county). Adds total_pop, household_pop, group_quarters_pop, housing unit breakdowns

### Output

Combined parquet with ~49 columns per county-day. One file per year, stored in 04_COMB_DATA_PARQ/. These files are later concatenated for model training.

---

## Stage 6: LOCA2 CMIP6 Processing for Inference (inference_data_loca2_processing)

### Purpose

Process CMIP6 climate projections from LOCA2 into the same county-level, population-weighted feature format as the historical URMA data, enabling the trained model to run inference on future climate scenarios.

### Data Source

LOCA2 statistically downscaled CMIP6 data on the cadcat S3 bucket (s3://cadcat/loca2/ucsd/), accessed anonymously via s3fs. Four variables per model-member-scenario: tasmax (daily max temperature), tasmin (daily min temperature), wspeed (wind speed), huss (specific humidity). Data is from the d03 (3 km) domain.

### Key Difference from URMA

LOCA2 does not provide cloud cover, dewpoint, or low wind speed. These features are dropped from inference. The model was designed to be robust to this — the features available in both URMA and LOCA2 (temperature, humidity, wind) carry the dominant predictive signal.

### Spatial Alignment

A county mask is built on the LOCA2 grid using the same TIGER 2023 county boundaries and spatial join approach as Stage 3. The WorldPop population grid is regridded from the URMA grid to the LOCA2 grid using nearest-neighbor interpolation so that the same population-weighting logic can be applied.

### Processing Function (process_one_run)

For each model-member combination, year by year (2015–2040), the four LOCA2 variables are loaded, reshaped to (time, pixel), masked to California-only pixels, then aggregated per county using both simple mean and population-weighted mean. Degree days (CDD65, CDD75, HDD65) are computed at the grid level before aggregation, matching the Stage 4 approach exactly. Each run produces a parquet with 17 climate features per county per day, plus model and member identifiers.

### Features Produced

tmax_k, tmax_k_pop, tmin_k, tmin_k_pop, tavg_k, trange_k, cdd65, cdd65_pop, cdd75, cdd75_pop, hdd65, hdd65_pop, spfh_peak_kgkg_mean, spfh_peak_kgkg_pop, wind_peak_ms_pop.

### Output Structure

One parquet per model-member-scenario combination, stored in separate directories by scenario (04_LOCA2_FEATURES/ for SSP370, 04_ssp245_LOCA2_FEAT/ for SSP245). These are then passed through the inference pipeline which adds non-weather features (data centers, BEV, population projections, calendar, baselines) and runs the trained ClimateFEAT model.

---

## Data Flow Summary

**Historical (training):** WorldPop TIF → URMA GRIB2 → zarr → county-aligned zarr → population-weighted feature zarr → parquet → merged with calendar + electricity + income + population → final training parquet

**Future (inference):** LOCA2 zarr on S3 → county-aggregated parquet per model-run → merge with projected data centers + BEV + population → inference pipeline → predicted MWh per county per day

---

## Technical Challenges and Decisions

**Longitude convention:** URMA uses 0–360 internally. Every spatial join requires conversion to -180/180 first. This was a recurring source of bugs throughout development.

**Zarr version compatibility:** Local zarr library versions on macOS sometimes conflicted with zarr stores written in Colab, requiring consolidated=False and explicit zarr_format parameters.

**iCloud sync corruption:** Local zarr stores synced via iCloud Desktop occasionally corrupted chunk files. Moving working data to a non-synced directory resolved this.

**Population weighting before vs after aggregation:** Degree days are computed on the raw grid before population-weighted aggregation to county. Computing degree days from county-mean temperatures would undercount extreme heat days in populous subregions of large, climatically diverse counties (e.g., San Bernardino).

**URMA analysis time selection:** UTC times were chosen to capture the specific meteorological conditions most relevant to electricity demand (afternoon peak for cooling load, overnight minimum for heating load), not arbitrary daily averages.