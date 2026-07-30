![logo](./notebooks/figures/LogoLine_horizon_C3S.png)


# Jupyter (note)books


This directory integrates the specific files for the C3S Atlas (note)Book and the [Jupyter notebooks](https://github.com/ecmwf-projects/c3s-atlas/tree/main/book/notebooks) to reproduce the [C3S Atlas Dataset](https://doi.org/10.24381/cds.h35hb680) and visual products of the [C3S Atlas Application](https://atlas.climate.copernicus.eu).

## Notebooks

Several Jupyter notebooks have been developed to explain how to reproduce the different indices and products underpinning the C3S Atlas. These notebooks build upon the [software](https://github.com/ecmwf-projects/c3s-atlas/tree/main/c3s_atlas) and [auxiliary information](https://github.com/ecmwf-projects/c3s-atlas/tree/main/auxiliar) included in the repository.

These notebooks are divided in three main groups: 
 - C3S Atlas Dataset (see Table 1): These notebooks focus on the end-to-end processing used to compute the different indices forming the ["gridded dataset underpinning the Copernicus Interactive Climate Atlas""](https://cds.climate.copernicus.eu/datasets/multi-origin-c3s-atlas?tab=overview). They describe and illustrate examples of indices with differetn requirements included in the C3S Atlas. These notebooks build on the Python function package included in the repository to facilitate the different processing steps: harmonization, aggregation, interpolation, etc.
 - C3S Atlas Application (see Table 2): These notebooks focus on the products visualized in the C3S Atlas (maps, time series, climatic stripes, etc.). They describe how to reproduce these products, as well as the auxiliary elements required, such as the calculation of Global Warming Levels (GWLs), the calculation of robustness/uncertainty layers, etc.
 - C3S Atlas Training (see Table 3): These notebooks provide training materials designed to introduce users to key aspects of climate change analysis, including the calculation and visualization of climate stripes and the assessment and interpretation of uncertainty in climate change projections.


| Directory | Contents |
| :-------- | :------- |
| [tx35.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/tx35.ipynb) | Jupyter Notebook for calculating the “number of days with maximum temperature over 35°C” (TX35) index using xclim library. | 
| [tx35bals.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/tx35bals.ipynb) | Jupyter Notebook for calculating “number of days with bias-adjusted maximum temperature over 35°C” (TX35bals) index using xclim and ibicus libraries. |
| [cd.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/cd.ipynb) | Jupyter Notebook for calculating the “Cooling Degree-Days” (CD) index using in-house index funtions. |
| [cddbaisimip.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/cddbaisimip.ipynb) | Jupyter Notebook for calculating the "Annual maximum consecutive dry days -below 1 mm" (CDD) with “bias-adjusted precipitation” (cddbaismip) index using the ISIMIP trend preserving method based on [Lange 2019](https://gmd.copernicus.org/articles/12/3055/2019/). |
| [pet.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/pet.ipynb) | Jupyter Notebook for calculating the “Monthly mean of daily accumulated potential evapotranspiration” (PET) index using the method described in [Hargreaves, G. H., and Samani, Z. A. (1985)](https://elibrary.asabe.org/abstract.asp??JID=3&AID=26773&CID=aeaj1985&v=1&i=2&T=1) using xclim library.|
| [spei6.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/spei6.ipynb) | Jupyter Notebook for calculating the “Monthly Standardised Precipitation-Evapotranspiration Index (SPEI) for 6 months cumulation period” (SPEI-6) index using xclim library.|

**Table 1.** Notebooks included as example to reproduce the C3S Atlas data production workflow.

| Directory | Contents |
| :-------- | :------- |
|  [customized_regions.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/customized_regions.ipynb) | Jupyter Auxiliary notebook with examples of how to produce regional results for customized regions defined in machine-readable formats (e.g. geojson).
|  [geographic_map.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/geographic_map.ipynb) | Jupyter Notebook for reproducing spatial maps of climatologies or changes for recent and future periods across emission scenarios or for different Global Warming Levels (GWL), including the calculation and display of robustness following the IPCC AR6 WGI methodology.
|  [time_series.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/time_series.ipynb) | Jupyter Notebook for reproducing regional time series for pre-defined regions.
|  [annual_cycle.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/annual_cycle.ipynb) | Jupyter Notebook for reproducing regional annual cycles for pre-defined regions.
|  [climate_stripe.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/climate_stripes.ipynb) | Jupyter Notebook for reproducing regional climate stripes for pre-defined regions.
|  [seasonal_stripe.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/seasonal_stripes.ipynb) | Jupyter Notebook for reproducing regional seasonal stripes for pre-defined regions.
|  [UHI.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/UHI.ipynb) | Jupyter Notebook to reproduce the Urban Climate analysis shown in the C3S Atlas.
|  [GWLs.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/GWLs.ipynb) | Auxiliary Jupyter Notebook illustrating the calculation of Global Warming Levels (GWLs), following the IPCC AR6 WGI methodology. This is used by the previous notebooks for calculating changes for different warming levels.

**Table 2.** Notebooks included as example to reproduce the C3S Atlas Application visual products.

| Directory | Contents |
| :-------- | :------- |
|  [climate_stripes_training.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/climate_stripes_training.ipynb) | Jupyter training notebook for calculating and visualizing climate stripes over the Mediterranean region using ERA5 reanalysis data and CMIP6 global climate model simulations.
|  [precipitation_uncertainty_training.ipynb](https://github.com/ecmwf-projects/c3s-atlas/blob/main/book/notebooks/precipitation_uncertainty_training.ipynb) | Jupyter training notebook for calculating long-term regional precipitation projections under the SSP5-8.5 scenario and assessing their associated uncertainty using a CMIP6 multi-model ensemble. The notebook reproduces selected results from the regional component of the C3S Atlas and compares precipitation changes and uncertainty across the Mediterranean and Western Africa regions.

**Table 3.** Notebooks including training materials for the C3S Atlas.





