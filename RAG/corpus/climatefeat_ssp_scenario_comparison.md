# ClimateFEAT SSP Scenario Comparison

## Overview

ClimateFEAT runs inference across two CMIP6 emissions scenarios to project future electricity demand under different climate trajectories. The comparison between SSP370 and SSP245 answers a key infrastructure planning question: does the emissions pathway matter for California electricity planning in the near term? The answer, supported by climate science and confirmed by our results, is that it does not — peak demand increases substantially regardless of scenario through 2040, and the infrastructure buildout needed is scenario-independent on this planning horizon.

---

## Shared Socioeconomic Pathways

The Shared Socioeconomic Pathways (SSPs) replaced the older Representative Concentration Pathways (RCPs) in the CMIP6 generation of climate models. SSPs provide a broader view of potential futures by incorporating societal changes, demographics, and economic factors alongside emissions trajectories.

**SSP2-4.5 ("Middle of the Road"):** 4.5 watts per meter squared of radiative forcing by 2100. Emissions continue at present levels to mid-century and then decline. Projected outcome: approximately 2.7°C warmer at end of century. This is the scenario most commonly used in policy-aligned climate analysis.

**SSP3-7.0 ("Regional Rivalry"):** 7.0 watts per meter squared of radiative forcing by 2100. Emissions roughly double from current levels by 2100 under conditions of nationalism, regional conflict, and slow economic development. Projected outcome: approximately 3.6°C warmer at end of century. This is the stress-test scenario relevant for utility infrastructure planners who need to account for 20-30 year asset lifespans.

Together, SSP245 and SSP370 bracket the range that most infrastructure planners consider actionable. SSP585 (8.5 W/m², emissions doubling by 2050, 4.4°C warming) was excluded from ClimateFEAT due to limited model availability in LOCA2 for our ensemble members.

---

## Sources of Uncertainty

According to Cal-Adapt Analytics Engine guidance, which uncertainty source dominates depends on the projection timescale. Internal variability (unpredictable weather) dominates for periods less than 10 years. Model uncertainty (which GCM best represents reality) dominates between 10 and 40 years. Scenario uncertainty (what societies choose to do about emissions) only becomes the dominant factor for periods longer than 40 years.

ClimateFEAT's projection window is 2025–2040, placing it squarely in the model uncertainty regime. This means the choice of GCM matters more than the choice of SSP at this timescale, which is why the multi-model ensemble approach is critical and why the SSP245 vs SSP370 convergence in our results is physically expected.

---

## Downscaling: LOCA2

ClimateFEAT uses LOCA2 (Localized Constructed Analogs, version 2) statistically downscaled CMIP6 data, developed by David W. Pierce at Scripps Institution of Oceanography. LOCA2 at 6 km resolution for the North American domain was completed in late 2022 and is one of the downscaled datasets used to inform the Fifth National Climate Assessment (NCA5). The generation of California-specific high-resolution data was supported by the California Energy Commission (EPC-20-006).

### LOCA2 Specifications

6 km spatial resolution, daily Tmin/Tmax/Precipitation, coverage from 1950 through 2100. SSP245, SSP370, and SSP585 are included where the original GCM ran those scenarios. The full LOCA2 dataset spans 27 models, 99 model-experiment combinations, and 329 individual ensemble members totaling 26,026 model-years.

ClimateFEAT accesses LOCA2 data via the cadcat S3 bucket (s3://cadcat/loca2/ucsd/) which hosts the California-specific subset.

---

## CMIP6 Ensemble Composition

Both scenarios use the same ensemble of 7 CMIP6 global climate models with 24-25 total runs: ACCESS-CM2 (1 member), EC-Earth3 (2 members), EC-Earth3-Veg (4 members), GFDL-ESM4 (1 member), INM-CM5-0 (5 members), MPI-ESM1-2-HR (6 members), and MRI-ESM2-0 (5 members). Models and members were selected based on availability of both SSP245 and SSP370 in LOCA2 with the required climate variables. Using multiple models captures structural uncertainty — different GCMs represent different physical assumptions about atmospheric processes, ocean circulation, and feedback mechanisms.

### SSP370 Ensemble (24 runs, 7 models)

- ACCESS-CM2: r1i1p1f1 (1 member)
- EC-Earth3: r1i1p1f1, r4i1p1f1 (2 members)
- EC-Earth3-Veg: r1i1p1f1, r2i1p1f1, r3i1p1f1, r4i1p1f1 (4 members)
- GFDL-ESM4: r1i1p1f1 (1 member)
- INM-CM5-0: r1i1p1f1, r2i1p1f1, r3i1p1f1, r4i1p1f1, r5i1p1f1 (5 members)
- MPI-ESM1-2-HR: r1i1p1f1, r2i1p1f1, r3i1p1f1, r4i1p1f1, r5i1p1f1, r10i1p1f1 (6 members)
- MRI-ESM2-0: r1i1p1f1, r2i1p1f1, r3i1p1f1, r4i1p1f1, r5i1p1f1 (5 members)

Total SSP370 rows: 11,694,192 (58 counties × daily × 24 runs × 2018–2040).

### SSP245 Ensemble (15 runs, 7 models)

- ACCESS-CM2: r1i1p1f1 (1 member)
- CNRM-ESM2-1: r1i1p1f2 (1 member)
- EC-Earth3: r1i1p1f1, r2i1p1f1, r4i1p1f1 (3 members)
- EC-Earth3-Veg: r1i1p1f1, r2i1p1f1, r3i1p1f1, r4i1p1f1, r5i1p1f1 (5 members)
- GFDL-ESM4: r1i1p1f1 (1 member)
- INM-CM5-0: r1i1p1f1 (1 member)
- MPI-ESM1-2-HR: r1i1p1f1, r2i1p1f1 (2 members)
- MRI-ESM2-0: r1i1p1f1 (1 member)

Total SSP245 rows: 7,308,870 (58 counties × daily × 15 runs × 2018–2040).

### Ensemble Asymmetry

The SSP245 ensemble is smaller because fewer GCMs ran SSP245 with multiple ensemble members in LOCA2. Six models overlap between scenarios (ACCESS-CM2, EC-Earth3, EC-Earth3-Veg, GFDL-ESM4, INM-CM5-0, MPI-ESM1-2-HR, MRI-ESM2-0). SSP245 adds CNRM-ESM2-1 which was not available for SSP370. The asymmetry in ensemble size means SSP370 has better-characterized internal variability (more members per model), while SSP245 has slightly broader model diversity. For the scenario comparison, results are aggregated at the ensemble-mean level so the different sample sizes do not bias the comparison.

---

## Historical Overlap Validation (2018–2023)

Both SSP245 and SSP370 produce nearly identical results in the historical period, as expected. The two emissions pathways have not yet diverged in cumulative atmospheric greenhouse gas concentrations during this period. Both scenarios show a consistent ~4-5°F warm bias on top-5% peak temperature days compared to URMA observations, with nearly identical patterns year over year. This warm bias is structural to the CMIP6 models over California and is scenario-independent — confirming that any performance differences between scenarios in the projection period are driven by genuine climate divergence rather than artifacts.

---

## Key Finding: Scenario Convergence Through 2040

The SSP370 and SSP245 ensemble mean projections track nearly on top of each other from 2018 through 2040, both showing statewide average predicted peak demand (top 20% of days) rising from approximately 54,000 MWh to approximately 74,000 MWh. This represents roughly a 40% increase in peak electricity demand regardless of which emissions pathway materializes.

The ensemble spread within each scenario is substantial — individual model runs range from approximately 49,000 to 80,000 MWh by 2040 — but the two scenario means remain within each other's confidence bands throughout the projection period. The scenarios do not meaningfully diverge by 2040.

This convergence is the physically expected result. The cumulative emissions difference between SSP245 and SSP370 has not had sufficient time to produce meaningfully different regional temperatures by 2040. Global temperature divergence between these scenarios is small before mid-century, and California-specific temperature differences are even smaller at this timescale.

### Policy Implication

California faces substantially higher peak electricity demand by 2040 under any plausible emissions scenario. The infrastructure investment needed is scenario-independent in the near term. This removes the rationale for delaying grid buildout while waiting to see which emissions pathway unfolds. To observe meaningful scenario divergence, projections would need to extend to 2060 or beyond, where scenario uncertainty becomes the dominant factor.

---

## Citations and References

- **LOCA2 downscaling:** Pierce, D.W., Scripps Institution of Oceanography, LOCA version 2 for North America. https://loca.ucsd.edu/loca-version-2-for-north-america-ca-jan-2023/. Full bibliography: https://loca.ucsd.edu/loca-bibliography/
- **SSP scenario definitions and California climate guidance:** Cal-Adapt Analytics Engine, Guidance on Climate Projections and Models. https://analytics.cal-adapt.org/guidance/about_climate_projections_and_models
- **SSP framework:** Carbon Brief explainer on Shared Socioeconomic Pathways. https://www.carbonbrief.org/explainer-how-shared-socioeconomic-pathways-explore-future-climate-change/
- **Model selection for California's Fifth Climate Change Assessment:** Krantz et al. 2021. https://www.energy.ca.gov/media/7264
- **CEC data center forecasts:** 2024 Final Data Center Forecast (https://www.energy.ca.gov/sites/default/files/2025-03/Data_Center_Forecast_Final_ada.pdf) and 2025 IEPR Preliminary Data Center Forecast (https://www.energy.ca.gov/sites/default/files/2025-11/2025_IEPR_Preliminary_Data_Center_Forecast_ada.pdf)