![logo](./notebooks/figures/LogoLine_horizon_C3S.png)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecmwf-projects/c3s-atlas/tree/main/HEAD?urlpath=%2Fdoc%2Ftree%2Fhttps%3A%2F%2Fgithub.com%2Fecmwf-projects%2Fc3s-atlas%2Fblob%2Fmain%2Fbook%2Ftx35.ipynb)

# User-tools for the [C3S Atlas](https://atlas.climate.copernicus.eu/atlas)

The user tools of the [C3S Atlas](https://atlas.climate.copernicus.eu/atlas) have been developed to enhance transparency and facilitate the reusability of the software developed to produce the [C3S Atlas Dataset](https://doi.org/10.24381/cds.h35hb680) and the visual products displayed in the [C3S Atlas Application](https://atlas.climate.copernicus.eu). These tools implement FAIR principles (Findability, Accessibility, Interoperability, and Reusability; [Iturbide et al. 2022](https://doi.org/10.5194/essd-12-2959-2020)).


## The C3S Atlas (note)Book

This Jupyter Book integrates and documents various notebooks available in the [c3s-atlas GitHub repository](https://github.com/ecmwf-projects/c3s-atlas), explaining how to reproduce the different indices and products underpinning the C3S Atlas. These notebooks build upon the software and auxiliary information included in the repository.

This book is divided into two main chapters: 
 - [C3S Atlas Dataset](./_build/html/chapter01.html): This chapter focuses on the end-to-end processing followed to compute the different indices forming the ["gridded dataset underpinning the Copernicus Interactive Climate Atlas""](https://cds.climate.copernicus.eu/datasets/multi-origin-c3s-atlas?tab=overview). It describes some Jupyter Notebooks with illustrative examples of indices with differetn requirements included in the C3S Atlas. These notebooks build on the Python function package included in the repository to facilitate the different processing steps: harmonization, aggregation, interpolation, etc.
 - [C3S Atlas Application](./_build/html/chapter02.html): This chapter focuses of the products visualized in the C3S Atlas (maps, time series, climatic stripes, etc.). It describes several Jupyter Notebooks to reproduce these products, as well as the auxiliary elements required, such as the calculation of Global Warming Levels (GWLs), the calculation of robustness/uncertainty layers, etc.

The Jupyter Book and the “c3s-atlas" GitHub repository serve as an initial package of user tools enabling reproducibility and reusability for the C3S Atlas. 


## The C3S Atlas GitHub repository

Table 1 shows the structure of the [c3s-atlas GitHub repository](https://github.com/ecmwf-projects/c3s-atlas).

| Directory | Contents |
| :-------- | :------- |
|  [auxiliar](https://github.com/ecmwf-projects/c3s-atlas/tree/main/auxiliar) | Auxiliary information and datasets, including GeoJSONs for pre-defined regions, spatial masks, etc.
|  [c3s_atlas](https://github.com/ecmwf-projects/c3s-atlas/tree/main/c3s_atlas) | Python functions and wrappers to reproduce the workflow for data production of the C3S Atlas.
|  [book](https://github.com/ecmwf-projects/c3s-atlas/tree/main/book) | Jupyter notebooks building on the sofware and auxiliary information to illustrate the calculation of indices of the dataset and visual products of the application.

**Table 1**. Table of contents of the  [“c3s-atlas" GitHub repository](https://github.com/ecmwf-projects/c3s-atlas).

### How to run the notebooks

[Scripts](https://github.com/ecmwf-projects/c3s-atlas/tree/main/c3s_atlas) and [Jupyter-Notebooks](https://github.com/ecmwf-projects/c3s-atlas/tree/main/book) are provided in [Python](https://www.python.org/) to ensure reproducibility and reusability of the results. Jupyter-Notebooks aim primarily for transparency and traceability, while the scripts contain functions and wrappers that are part of the workflow designed for the C3S Atlas.

The simplest way to run the notebooks is by using a dedicated [conda](https://docs.conda.io) environment, which can be installed with the following commands:

```sh
git clone git@github.com:ecmwf-projects/c3s-atlas.git
conda create -n c3s-atlas
conda activate c3s-atlas
cd c3s-atlas
conda env update --file environment.yml --prune
pip install -e .
```

A much straigtforward way to explore and interact with this repository is through binder. Binder provides an executable environment, making the code immediately reproducible. The required software is pre-installed in a cloud environment where the user can create and execute notebooks (directly) and scripts (via the available Terminal). Moreover, the environment is accessible without any further authentication by the user.

To start exploring the binder interface, just click the Launch in MyBinder badge above. You will arrive at a JupyterLab interface with access to the contents of this repository.

## The C3S Atlas

The [C3S Atlas](http://atlas.climate.copernicus.eu) is an application of the  Copernicus Climate Change Service (C3S) which enables an interactive exploration of the Earth's climate, from recent changes and trends to possible climate futures under different emission scenarios. It uses key datasets that are available in the C3S Climate Data Store (CDS), including observation-based datasets (E-OBS), reanalyses (ECMWF’s ERA5, ERA5-Land and ORAS5), and comprehensive global (CMIP5/6) and regional (CORDEX) climate projections. The C3S Atlas is a new resource for policy makers wishing to formulate effective climate policy and for other users who need to visualise and analyse climate change information, particularly at the regional scale. This C3S tool is an evolution of the Intergovernmental Panel on Climate Change (IPCC) Interactive Atlas (IPCC-IA), which was frozen in 2021 with the publication of the Sixth Assessment Report’s (AR6) WGI (Working Group I) section (see https://www.ipcc.ch/report/ar6/wg1).

A brief description of the C3S Atlas is available in the ECMWF Newsletter 181 ([Gutiérrez et al. 2024](https://doi.org/10.21957/ah52ufc369), [online document](https://www.ecmwf.int/en/newsletter/181/earth-system-science/copernicus-interactive-climate-atlas-tool-explore-regional)).





