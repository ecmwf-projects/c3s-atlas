![logo](./book/notebooks/figures/LogoLine_horizon_C3S.png)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecmwf-projects/c3s-atlas/main?urlpath=%2Fdoc%2Ftree%2Fbook%2Fnotebooks%2Ftx35.ipynb)

# C3S Atlas User Tools

The [C3S Atlas](https://atlas.climate.copernicus.eu) user-tools GitHub repository has been developed to enhance transparency and facilitate the reusability of the software developed to produce the [C3S Atlas Dataset](https://doi.org/10.24381/cds.h35hb680) and the visual products displayed in the [C3S Atlas Application](https://atlas.climate.copernicus.eu), implementing FAIR principles (Findability, Accessibility, Interoperability, and Reusability; [Iturbide et al. 2022](https://doi.org/10.5194/essd-12-2959-2020)).

## The C3S Atlas

The [C3S Atlas](http://atlas.climate.copernicus.eu) is an application of the  Copernicus Climate Change Service (C3S) which enables an interactive exploration of the Earth's climate, from recent changes and trends to possible climate futures under different emission scenarios. It uses key datasets that are available in the C3S Climate Data Store (CDS), including observation-based datasets (E-OBS), reanalyses (ECMWF’s ERA5, ERA5-Land and ORAS5), and comprehensive global (CMIP5/6) and regional (CORDEX) climate projections. The C3S Atlas is a new resource for policy makers wishing to formulate effective climate policy and for other users who need to visualise and analyse climate change information, particularly at the regional scale. This C3S tool is an evolution of the Intergovernmental Panel on Climate Change (IPCC) Interactive Atlas (IPCC-IA), which was frozen in 2021 with the publication WGI contribution (Working Group I; see https://www.ipcc.ch/report/ar6/wg1) of the Sixth Assessment Report’s (AR6).

A brief description of the C3S Atlas is available in the ECMWF Newsletter 181 ([Gutiérrez et al. 2024](https://doi.org/10.21957/ah52ufc369), [online document](https://www.ecmwf.int/en/newsletter/181/earth-system-science/copernicus-interactive-climate-atlas-tool-explore-regional)).

## The C3S Atlas GitHub repository

The table below shows the structure of the [c3s-atlas GitHub repository](https://github.com/ecmwf-projects/c3s-atlas).

| Directory | Contents |
| :-------- | :------- |
|  [auxiliar](https://github.com/ecmwf-projects/c3s-atlas/tree/main/auxiliar) | Auxiliary information and datasets, including GeoJSONs for pre-defined regions, spatial masks, etc.
|  [c3s_atlas](https://github.com/ecmwf-projects/c3s-atlas/tree/main/c3s_atlas) | Python functions and wrappers to reproduce the workflow for data production of the C3S Atlas.
|  [book](https://github.com/ecmwf-projects/c3s-atlas/tree/main/book) | Jupyter notebooks building on the sofware and auxiliary information to illustrate the calculation of indices of the dataset and visual products of the application.

## Requirements

Scripts and (jupyter) notebooks are provided in [Python](https://www.python.org/) to ensure reproducibility and reusability of the results. The simplest way to meet all these requirements is by using a dedicated [conda](https://docs.conda.io) environment, which can be easily installed by issuing:

```sh
git clone git@github.com:ecmwf-projects/c3s-atlas.git
conda create -n c3s-atlas
conda activate c3s-atlas
cd c3s-atlas
conda env update --file environment.yml --prune
pip install -e .
```

The following Python libraries have been used for the implementation of the workflow and the user-tools repository.

| Library  | Description |
|----------|-------------|
| [xclim](https://xclim.readthedocs.io/en/stable/) | xclim is a library for climate index calculation built using xarray and can seamlessly benefit from the parallelization handling provided by dask. |
| [ibicus](https://ibicus.readthedocs.io/en/latest/index.html) | Bias adjustment library for climate model data adjustment using observational references. | 
| [xESMF](https://xesmf.readthedocs.io/en/stable/) | Regridding library for geospatial data | 
| [xarray](https://docs.xarray.dev/en/stable/) | Python library for managing labelled multi-dimensional arrays |
| [dask](https://examples.dask.org/xarray.html) | Python library for parallel computing | 
| [cdsapi](https://cds.climate.copernicus.eu/how-to-api) | The Climate Data Store (CDS) Application Program Interface (API) is a service providing programmatic access to CDS data. |

A straightforward way to explore and interact with this repository online is by using Binder. Binder offers an executable environment with free but limited resources, allowing you to immediately reproduce the code without needing to install software locally. The required software comes pre-installed in a cloud-based environment, enabling you to directly create and execute notebooks and run scripts through the provided Terminal. Additionally, this environment is freely accessible without requiring any user authentication. To begin exploring via Binder, simply click on the "Launch in MyBinder" badge above. 

## License

```
Copyright 2023, European Union.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

