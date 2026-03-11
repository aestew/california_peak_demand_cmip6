# CEC Demand Forecasting Background

## What This Document Covers

This document describes how the California Energy Commission (CEC) currently forecasts electricity demand, the regulatory context that drives the forecast, how weather and climate data enter the process, where the current methodology falls short on climate integration, and where ClimateFEAT addresses those gaps. Primary source: Final 2024 Integrated Energy Policy Report Update (CEC-100-2024-001-LCF, September 2025), authored by Stephanie Bailey, Mathew Cooper, Quentin Gee, Heidi Javanbakht, Jake McDermott, and Danielle Mullany.

## The Institutional Landscape

California's electricity planning involves three primary agencies, each consuming the CEC demand forecast for different purposes.

The California Energy Commission (CEC) produces the official California Energy Demand (CED) forecast as part of the biannual Integrated Energy Policy Report (IEPR). This is the authoritative statewide demand projection used for all downstream planning. The Energy Assessments Division manages the forecast, led by Heidi Javanbakht (Demand Analysis Branch Manager) with Sandra Nakagawa as IEPR Director. Nick Fugate leads the hourly and peak electricity demand forecast. Lakemariam (Lake) Worku advises on climate change data inputs to the forecast. The forecast is developed through a public process including Demand Analysis Working Group (DAWG) meetings and IEPR workshops, then adopted at a public CEC business meeting. The 2024 IEPR Update forecast was adopted January 21, 2025 and covers 2024–2040.

The California Public Utilities Commission (CPUC) uses the CEC forecast as an input to the Integrated Resource Plan (IRP), which determines how much generation capacity the state needs and directs procurement by the investor-owned utilities (PG&E, SCE, SDG&E). The CPUC also uses the forecast for resource adequacy requirements, which shifted to a Slice of Day framework in 2025 requiring hourly load profiles rather than just annual and monthly peaks.

The California Independent System Operator (CAISO) manages roughly 80% of California's electricity load. CAISO uses the CEC forecast for its annual Transmission Planning Process (TPP), Summer Loads and Resources Assessment, and flexible capacity needs assessment. From 2014 to 2024, CAISO actual annual peak demand ranged between approximately 43,800 MW and 51,500 MW.

The three agencies have a formal Memorandum of Understanding (December 2022) agreeing that specific elements of the CEC forecast set will be used for planning and procurement across their respective proceedings.

## How the CEC Currently Forecasts Demand

The CEC forecast is sector-based, with different modeling approaches for each segment of electricity consumption:

Residential: End-use model calibrated by econometric model. This bottom-up approach models individual end uses (air conditioning, heating, lighting, appliances) and their adoption and efficiency trajectories, then calibrates total consumption against econometric relationships with economic and demographic drivers.

Commercial: Econometric model (with an end-use model in development that will incorporate 2018–2022 Commercial End-Use Survey data).

Industrial (manufacturing, mining, construction): Econometric models by NAICS code. The 2023 results were calibrated with 2024 inputs.

Agriculture, cannabis, water pumping: Econometric models by NAICS code.

Transportation, communication, utilities, streetlighting: Trend analysis. The 2023 results were calibrated with 2024 inputs.

Historical energy consumption data is the foundation. Staff establishes correlations between historical consumption and economic/demographic data, weather data, and electricity rates, specific to each forecast zone and economic sector. Projections for future economic and demographic trends, weather, and rates are then used with those historical correlations to extend consumption into the future.

Key economic and demographic inputs for the 2024 forecast: California population of 39.2 million in 2024, projected to reach 41.3 million by 2040 (0.3% annual growth). Households growing at 0.6% annually, reaching 15.2 million by 2040. Gross state product growing at 1.8% annually, reaching $5.3 trillion by 2040. Per capita personal income reaching $108,300 by 2040 (1.8% annual growth).

## The Forecast Framework: Planning vs Local Reliability

The CEC produces two managed forecast scenarios from the same baseline, designed for different planning contexts.

The Planning Forecast uses mid-case BTM PV and storage, mid-case data centers, and AAEE/AAFS/AATE Scenario 3 (reasonably expected policy impacts plus programs "very likely to occur with greater uncertainty about impact magnitudes"). This scenario is used for CPUC integrated resource planning and CAISO system resource adequacy with 1-in-2 weather conditions, and for CAISO bulk system transmission studies with 1-in-5 weather conditions.

The Local Reliability Scenario uses low-case BTM PV (less solar generation means higher net demand), high-case data centers, AAEE Scenario 2 (less efficiency savings), AAFS Scenario 4 (more fuel substitution), and AATE Scenario 3. This produces higher demand numbers and is used for CAISO transmission planning local area reliability studies and IOU distribution planning with 1-in-10 weather conditions — contexts where planning conservatively for higher demand is appropriate.

The forecast also includes six additional achievable scenario levels for energy efficiency and fuel substitution, ranging from Scenario 1 (firm commitments only) through Scenario 6 (programs that could exist and would be required to meet policy goals).

## Load Modifiers

On top of the baseline, several load modifiers are layered:

Behind-the-meter PV and storage: By end of 2023, an estimated 17.2 GW of BTM PV capacity was installed in California. The 2024 IEPR Update revised BTM PV capacity factors downward using metered generation data from a large real-world sample — annual capacity factors for the CAISO region dropped from roughly 21% to 18%, reducing estimated annual BTM PV generation by 1,400 to 2,400 GWh in historical years. BTM PV paired with energy storage reached 69% of residential net billing tariff interconnections in 2024 due to the incentive structure of the NBT that went into effect April 2023.

Additional Achievable Energy Efficiency (AAEE): Scenario 3 saves approximately 13,500 GWh by 2040 across all sectors.

Additional Achievable Fuel Substitution (AAFS): Driven overwhelmingly by the zero-emission space and water heater standard component (CARB's proposed zero-GHG regulations, plus BAAQMD and SCAQMD zero-NOx rules). The ZE standard adds roughly 25 times more electricity than programmatic fuel substitution by 2040. Combined AAEE and AAFS produce a net increase of approximately 28,800 GWh in the Planning Forecast by 2040 — energy efficiency savings are only about one-third the size of added load from fuel substitution.

Additional Achievable Transportation Electrification (AATE): Light-duty ZEV population exceeds 1.5 million as of 2023 with new vehicle sales at approximately 25% ZEV. Under AATE Scenario 3, light-duty ZEV population reaches 14.6 million by 2035 (versus 7.4 million in baseline). AATE adds approximately 44,000 GWh by 2040 in both the Planning Forecast and Local Reliability Scenario. More than 1.5 million heat pumps estimated installed in California as of 2023; both forecast scenarios project achieving the 6 million heat pump goal by 2030.

## 2024 Forecast Results

Statewide electricity consumption was more than 276,000 GWh in 2023. Key 2040 projections:

Planning Forecast: Baseline consumption reaches 395,870 GWh. Baseline sales reach 338,309 GWh. Managed sales (with all load modifiers) reach 411,121 GWh. CAISO system peak demand reaches 66,798 MW (2.3% annual growth).

Local Reliability Scenario: Baseline consumption reaches 400,892 GWh. Baseline sales reach 347,626 GWh. Managed sales reach 420,154 GWh. CAISO system peak demand reaches 68,519 MW.

The 2024 IEPR Update forecast is substantially higher than the 2023 IEPR: baseline sales are 13% higher in the Planning Forecast and 16% higher in the Local Reliability Scenario, driven primarily by data center growth and reduced BTM PV generation assumptions. The CAISO managed system peak is 11.3% higher than the 2023 IEPR Planning Forecast by 2040.

## Data Center Forecast

Data centers represent the single largest driver of forecast growth. The CEC received application data from five utilities: Silicon Valley Power, City of Palo Alto, City of San Jose, PG&E, and SCE. LADWP, SMUD, and SDG&E were consulted but showed no significant data center growth in their territories.

PG&E reported roughly 4,000 MW in large load applications, mostly from data centers. SCE reported growth ranging from 100+ MW to 500+ MW over five years.

Applications are categorized by stage: T&D Planning (completed engineering studies, in development), Group 1 (active application with engineering study completed or underway), Group 2 (active application prior to engineering study), Group 3 (project inquiries without formal application).

Confidence levels applied by scenario: Low — T&D Planning at 100%, Group 1 at 50%. Mid — T&D Planning at 100%, Group 1 at 70%, Group 2 at 50%. High — T&D Planning at 100%, Group 1 at 70%, Group 2 at 50%, Group 3 at 10% (PG&E) or 10-50% (SCE).

A utilization factor of 67% converts requested capacity to estimated peak load, based on Silicon Valley Power's analysis of more than 60 existing data centers of various types within their territory.

Annual data center peak demand growth: roughly 15% (low), 19% (mid), 20% (high) from 2024 to 2030. Nearly 63% of projected load growth by 2040 is in PG&E territory. Data centers alone add more than 3,000 MW to CAISO peak demand by 2040. The Planning Forecast includes 27,000 GWh of incremental data center load versus 2023; the Local Reliability Scenario includes 32,000 GWh.

Load growth flattens after 2035 because the CEC did not model a long-term growth rate beyond utility application queues due to high uncertainty. Multiple stakeholders commented that projections may be too low because they don't account for new applications arriving after the data cutoff, long-term growth trends, or redundancy needs when out-of-state data centers go offline.

## How Weather and Climate Enter the Current Forecast

The CEC's forecast relies on weather normalization — establishing "normal" weather conditions from historical weather station data, then using those normals as the baseline for demand correlations. Peak demand is forecast at multiple exceedance levels: 1-in-2 (median weather year), 1-in-5, 1-in-10, and 1-in-20 (extreme weather year). These weather variants are derived from historical weather patterns. Different planning processes use different variants: CPUC IRP uses 1-in-2, CAISO bulk system studies use 1-in-5, CAISO local reliability uses 1-in-10.

Beginning with the 2023 IEPR, the CEC began incorporating downscaled climate projections using the Weather Research and Forecasting (WRF) model at 3 km resolution, localized to specific weather stations within the CEC's forecast models. The 2023 IEPR used four WRF model runs: CESM2 r11i1p1f1, CNRM-ESM2 r1i1p1f2, EC-Earth3-Veg r1i1p1f1, and FGOALS-g3 r1i1p1f1.

Four additional WRF model runs became available during the 2024 IEPR cycle: EC-Earth3 r1i1p1f1, MIROC6 r1i1p1f1, MPI-ESM1-1-HR r3i1p1f1, and TaiESM1 r11i1p1f1. These new runs show significantly higher annual CDD and lower annual HDD for the CAISO region compared to the original four models.

## The Climate Gap

The IEPR states explicitly: "The increased warming trend is too significant a change to implement during a forecast update and requires further review by staff and stakeholders." The CEC chose to continue using only the original four WRF models for the 2024 forecast, deferring the warmer projections to the full 2025 IEPR forecast cycle where staff can explore transitioning to the new WRF output with stakeholder input.

This is the central gap that ClimateFEAT addresses. The CEC has climate projections showing substantially higher cooling demand, but the magnitude of the change is too large for their existing econometric framework to absorb. The econometric models establish statistical correlations from historical weather-demand relationships and project forward — when the climate inputs shift dramatically outside the historical training distribution, the correlations become unreliable. The models were not designed to handle nonstationary climate inputs.

As Lake Worku (CEC) stated at the July 2024 IEPR workshop on forecast methodology (docket 24-IEPR-03): understanding and incorporating future impacts of climate change on California's electricity and gas demand is critical, but climate change uncertainty complicates the practice of using historical weather data to establish normal weather conditions.

Specific limitations of the current approach:

Weather station-based spatial resolution: The CEC maps weather station data to planning areas and forecast zones using fixed weights. This misses subregional climate variation within large planning areas. ClimateFEAT uses 2.5 km (URMA) and 3-6 km (LOCA2) gridded data population-weighted to all 58 counties.

Historical normals as baseline: The CEC's weather normalization assumes stationarity — that past weather distributions predict future ones. ClimateFEAT directly ingests CMIP6 projections that capture nonstationary trends.

Linear econometric relationships: The CEC's econometric models assume stable, typically linear relationships between weather variables and demand. ClimateFEAT's transformer architecture with cross-attention fusion captures nonlinear interactions — how humidity amplifies cooling demand response to temperature, how sustained multi-day heat events create compounding demand beyond what single-day degree day models capture.

Sector-based aggregation: The CEC models sectors separately and sums. ClimateFEAT models total county-level demand directly, capturing cross-sector interactions.

Limited climate model ensemble: The CEC currently uses 4 WRF model runs (with 4 more deferred) under a single emissions scenario (SSP370). ClimateFEAT runs 24-25 ensemble members across two scenarios (SSP370 and SSP245), providing both model uncertainty bounds and scenario comparison.

## Where ClimateFEAT Fits In

ClimateFEAT is not a replacement for the CEC forecast. It is a complementary tool that could improve the climate data inputs to the existing framework.

County-level climate-informed demand projections could serve as an independent cross-check on the CEC's planning area forecasts, flagging counties where climate-driven demand growth may be underestimated.

The multi-scenario SSP comparison provides a framework for stress-testing demand forecasts under different emissions pathways — something the CEC does not currently do for the demand forecast. The CEC uses multiple weather exceedance levels (1-in-2 through 1-in-20) derived from historical patterns, but does not yet produce demand forecasts under different climate scenarios.

The population-weighted spatial aggregation methodology could improve how climate data is translated from gridded projections to the geographic units the CEC uses for planning. The CEC currently localizes WRF output to specific weather stations; ClimateFEAT uses continuous gridded fields weighted by where people actually live.

The data center load projections, built from facility-level historical data scaled by CEC TAC-level growth forecasts, provide a bottom-up validation of the top-down queue-based approach the CEC uses. ClimateFEAT incorporates data center capacity as a feature in its model, allowing it to capture interactions between infrastructure growth and climate-driven demand.

Notably, some of the same GCMs appear in both the CEC's WRF ensemble and ClimateFEAT's LOCA2 ensemble (EC-Earth3, MPI-ESM1-2-HR), providing a basis for cross-validation between the two approaches.

## RFP-25-803: Direct Alignment

In February 2026, the CEC released RFP-25-803, titled "Improvements to Modeling Climate Data in Demand Forecasting," through the Energy Assessments Division. The solicitation seeks to continue work on improving methods for preparing global climate model data inputs for use in the California energy demand forecast, including translating projections into forecast inputs, calculating impacts on annual and hourly demand, and analyzing impacts on peak demand and average levels of HDD and CDD. This describes ClimateFEAT's core functionality. The previous cycle of this work (EPC-20-006) was performed by Scripps Institution of Oceanography (LOCA2 downscaling) and UCLA (WRF downscaling).

## CEC Next Steps (from the IEPR)

For the 2025 IEPR: developing a probabilistic hourly electricity dataset to support resource planning, revisiting data center load growth assumptions, exploring incorporation of utility known load data for distribution planning, and improved geographic assignment of EV load across forecast zones.

For the 2026 IEPR Update and beyond: assessing industrial and agricultural fuel substitution including hydrogen, updating the commercial end-use model, incorporating agriculture vehicle survey data, new EV load shape tools, exploring increased geographic granularity to support local studies, and exploring demand flexibility tools and their interaction with the forecast.

## Key Contacts

Heidi Javanbakht — Demand Analysis Branch Manager, Energy Assessments Division. Primary author of the IEPR forecast chapter.

Nick Fugate — Leads the hourly and peak electricity demand forecast.

Lakemariam (Lake) Worku — Climate change data advisor for the demand forecast. Presented on weather and climate data in annual electricity consumption models at the July 2024 IEPR workshop.

Sandra Nakagawa — IEPR Director.

Demand Analysis Working Group: DAWG@energy.ca.gov.

## Key References

Final 2024 Integrated Energy Policy Report Update. CEC-100-2024-001-LCF. September 2025. https://www.energy.ca.gov/data-reports/reports/integrated-energy-policy-report-iepr/2024-integrated-energy-policy-report-0

IEPR Docket 24-IEPR-03: Electricity Demand Forecast proceedings. July 2024 methodology workshop on climate data integration. https://www.energy.ca.gov/event/workshop/2024-07/iepr-commissioner-workshop-energy-demand-forecast-methodology-updates

CEC demand forecast data and documentation: https://www.energy.ca.gov/data-reports/california-energy-planning-library/forecasts-and-system-planning/demand-side-2

CAISO 2025 Summer Loads and Resources Assessment: https://www.caiso.com/content/summer-loads-resources-assessment/2025/index.html

RFP-25-803: https://www.energy.ca.gov/solicitations/2026-02/rfp-25-803-improvements-modeling-climate-data-demand-forecasting

MOU between CPUC, CEC, and CAISO on Transmission and Resource Planning (December 2022): https://efiling.energy.ca.gov/GetDocument.aspx?tn=262057&DocumentContentId=98567