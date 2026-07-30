![logo](../book/notebooks/figures/LogoLine_horizon_C3S.png)

# c3s_atlas(in-house) python functions

This repository contains **source** functions and wrappers designed to reproduce the workflow for data production of the [C3S Atlas](https://atlas.climate.copernicus.eu/atlas). The functions in this repository facilitate various processing steps such as harmonization, aggregation, interpolation, and more.

Table 1 provides descriptions of the main files in the repository, outlining their functionality.

| **File**             | **Description**                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| `aggregation.py`      | Contains functions to aggregate data across different dimensions or time periods.
| `analysis.py`         | Includes functions for data analysis, such as calculating statistical properties, trends, and performing exploratory data analysis |
| `customized_regions.py`| Provides functions to define and handle custom regions for analysis, possibly including spatial subsetting or creating specific regional masks. |
| `errors.py`           | Contains error-handling functions to manage and log errors throughout the processing workflow, e.g. unable to infer the temporal frequency. |
| `fixers.py`           | Provides utility functions to fix or clean up data from different sources |
| `indexes.py`          | Includes in-house function for calculating various climate indices |
| `interpolation.py`    | Contains functions for regridding data to different spatial resolutions based on the [xESMF](https://xesmf.readthedocs.io/en/stable/) Regridding library |
| `logger.py`           | Includes functions for logging messages, warnings, and errors during the execution of the data processing pipeline. |
| `products.py`         | Contains functions to visualice the products available in the [C3S Atlas Application](./_build/html/chapter02.html). |
| `temporal.py`         | Includes functions to handle time-based operations |
| `units.py`            | Contains utility functions for unit conversions and ensuring consistency of units across the dataset. |

Table 1. In-house functions for the [C3S Atlas](https://atlas.climate.copernicus.eu/atlas).

## Homogenization

For consistency, the C3S Atlas undergoes a process of homogenization and standardization to merge different sources from reanalysis, observations, and projections.

- The metadata of the spatial coordinates is homogenised to use standard names, in particular [lon, lat].
- Fix any non-standard calendars used in the data. This typically involves converting the calendars to the CF standard calendar (Mixed Gregorian/Julian) commonly used in climate data.
- Convert the units of the data to a common format (e.g. Celsius for temperature). This prevents us from working with the same variables in different units, for example.
- Convert the longitude values from the [0, 360] format to the [-180, 180] one. This is done to ensure that the longitude variable is common between the different datasets.
- Aggregated to the required temporal resolution. For example, hourly datasets (such as ERA5, ERA5-Land, WFDE5, etc.) will be resampled to daily resolution. This involves using a temporal aggregation method, such as taking the maximum or minimum value for a given variable. As part of this last step, some variable transformations are necessarily applied. For instance, fluxes variables in ERA5 are accumulated, and therefore, the last hour of the day represent daily accumulations. To mention another case, the surface wind is computed as a combination of both the u- and v-components.





