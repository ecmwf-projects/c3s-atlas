import xarray as xr
import array as arr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import regionmask
import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
import regionmask
import cartopy.feature as cfeature
import scipy as sp

from c3s_atlas.utils import(
 count_years)

def mean_values_map(ds, var, model, mode,  diff = None, months=None, season=None,
                    period=slice('2081', '2100'),
                    baseline_period=slice('1981', '2010'), GWLs_ds = None):
    '''
    Divides the provided data into 3 categories of robustness for each latitude and longitude.

    Parameters
    ----------
    ds : xarray.Dataset
        The dataset containing the climate data.
    var : str
        The name of the variable to calculate robustness for.
    mode : str
        The mode of calculation. Can be 'climatology' or 'change'.
    model : str
        The model used for the calculations.
    diff : str
        The type of difference calculation. Can be 'abs' for absolute difference or 'rel' for relative difference.
    months : list, optional
        Specific months to include in the calculation. If provided, it overrides the season parameter. Default is None.
    season : str, optional
        The season for which to calculate the mean. Can be 'Annual', 'DJF', 'MAM', 'JJA', or 'SON'. Default is 'Annual'.
    period : slice, optional
        The period for which to calculate robustness. Default is slice('2081', '2100').
    baseline_period : slice, optional
        The baseline period for calculating the mean baseline. Default is slice('1981', '2010').
    ds_GWLs: xarray Dataset, optional
        The dataset containing the variable mean for global warning levels. Default is None.
    Returns
    -------
    ds_mean : xarray.DataArray
        The dataset with the mean values calculated according to the specified mode and difference type.
    '''
    
    # If specific months are provided, select only those months from the dataset
    if season:
        ds = ds.sel(time=ds['time.month'].isin(season))
        if GWLs_ds is not None:
            GWLs_ds = GWLs_ds.sel(month = GWLs_ds['month'].isin(season))
        
    # Calculate the mean based on the selected mode
    if model in ["ERA5", "ERA5-Land", "E-OBS", "ORAS5"]:# models that don't have member                          
        if mode == 'climatology':
            ds = ds.sel(time = period)
            ds_mean = ds[var].mean('time', skipna=True)
        elif mode == 'change':
            ds_baseline = ds[var].sel(time=baseline_period).mean('time', skipna=True)
            ds_period = ds[var].sel(time=period).mean('time', skipna=True)
            if diff == 'abs':
                ds_mean = ds_period - ds_baseline
            elif diff == 'rel':
                ds_mean = (ds_period - ds_baseline) / abs(ds_baseline) * 100
    else:
        if mode == 'climatology':
            ds_mean = ds[var].mean(dim=['time','member'], skipna=True)
        elif mode == 'change':
            if GWLs_ds is not None:
                ds_period = GWLs_ds[var].mean(dim=['month','member'], skipna=True)
            else:
                ds_period = ds[var].sel(time=period).mean(dim=['time','member'], skipna=True)
            ds_baseline = ds[var].sel(time=baseline_period).mean(dim=['time','member'], skipna=True)
            if diff == 'abs':
                ds_mean = ds_period - ds_baseline
            elif diff == 'rel':
                ds_mean = (ds_period - ds_baseline) / abs(ds_baseline) * 100
    return ds_mean

def categories_robustness(ds, var, months = None, season = None, period=slice('2081', '2100'),
                          baseline_period=slice('1981', '2010'), GWLs_ds = None):
    '''
    Divides the provided data into 3 categories of robustness for each latitude and longitude.

    Parameters
    ----------
    ds : xarray.Dataset
        Data stored by dimensions.
    var : str
        The name of the variable to calculate robustness for.
    months : list, optional
        Specific months to include in the calculation, overrides season if provided. Default is None.
    season : str, optional
        The season for which to calculate the mean ('Annual', 'DJF', 'MAM', 'JJA', 'SON').
    period : slice, optional
        The period for which to calculate robustness. Default is slice('2081', '2100').
    baseline_period : slice, optional
        The baseline period for calculating the mean baseline. Default is slice('1981', '2010').
    ds_GWLs: xarray Dataset, optional
        The dataset containing the variable grouped by month for global warning levels.. Default is None.
    Returns
    -------
    categories : xr.DataArray
        Matrix with the data divided into the categories.
    '''

    
     # If specific months are provided, select only those months from the dataset
    if season:
        ds = ds.sel(time=ds['time.month'].isin(season))
        if GWLs_ds is not None:
            GWLs_ds = GWLs_ds.sel(month = GWLs_ds['month'].isin(season))
    
    # Select the dataset for the given period
    if GWLs_ds is not None:
        mean_period = GWLs_ds[var].mean(dim=['month'], skipna=True)
        years_count = 20
    else:
        mean_period = ds[var].sel(time=period).mean(dim='time', skipna=True)
        # count the years of period
        years_count = count_years(period)
    
    # Select the dataset for the baseline period
    mean_baseline = ds[var].sel(time=baseline_period).mean(dim = 'time', skipna=True)
    
    # Change 
    change = mean_baseline - mean_period
    
    # Determine the sign of the change
    sign_change = np.sign(change)
    
    # Initialize an empty DataArray to store the sign of the change for each grid point
    sign_models = xr.DataArray(np.zeros_like(sign_change.isel(member=0)),
                               coords={'lat': sign_change['lat'], 'lon': sign_change['lon']},
                               dims=['lat', 'lon'])

    
    # Calculate the sum of the sign of the change for each grid point
    for i in sign_change['lon'].values:
        for j in sign_change['lat'].values:
            sign_models.loc[dict(lat=j, lon=i)] = sign_change.sel(lat=j, lon=i).sum()

                              
    # Select the dataset for 1971 -2005
    ds_reference_ys = ds.sel(time=slice('1971', '2005')).resample(time = 'YS').mean()
                              
    # Calculate the standard deviation of temperature across years
    std = ds_reference_ys.std(dim='time')

    # Calculate the variability using a specified threshold
    threshold = 1.645 * np.sqrt(2/years_count) * std #error
    
    # Create a mask to identify significant changes
    significant_change_mask = abs(threshold[var]) < abs(change)
    
    # Initialize a DataArray to count the number of models indicating significant change
    num_models = xr.DataArray(np.zeros_like(threshold[var].isel(member = 0)), 
                              coords={'lat': threshold['lat'], 'lon': threshold['lon']},
                              dims=['lat', 'lon'])   
                                  
    # Iterate over each latitude, longitude, and model
    for i in threshold['lon'].values:
        for j in threshold['lat'].values:
            for m in threshold['member'].values:
                # Increment the count if there is a significant change
                if significant_change_mask.sel(lat=j, lon=i, member=m).values:
                    num_models.loc[dict(lat=j, lon=i)] += 1  
                              
    # Calculate the total number of members
    total_members = len(ds['member'].values)
    
    # Create a DataArray to store the categories
    categories = xr.DataArray(np.zeros_like(threshold[var].isel(member = 0)), 
                                  coords={'lat': threshold['lat'], 'lon': threshold['lon']}, 
                                  dims=['lat', 'lon'])


    # Iterate over each longitude and latitude
    for i in num_models['lon'].values:
        for j in num_models['lat'].values:
            # Category (i): Areas with significant change and high model agreement
            # 60 because it is 1 and -1, so if 80% agrees it is 80% (same sign) 20% (other sign)
            if abs(sign_models.sel(lat=j, lon=i)) >= 0.60 * total_members and num_models.sel(lat=j, lon=i) >= (2/3) * total_members:
                categories.loc[dict(lat=j, lon=i)] = 1
            # Category (ii): Areas with no change or no robust change
            elif num_models.sel(lat=j, lon=i) < (2/3) * total_members:
                categories.loc[dict(lat=j, lon=i)] = 2
            # Category (iii): Areas with significant change but low agreement
            elif num_models.sel(lat=j, lon=i) >= (2/3) * total_members and abs(sign_models.sel(lat=j, lon=i)) < 0.60 * total_members:
                categories.loc[dict(lat=j, lon=i)] = 3
    
    return categories, sign_models, num_models

def annual_weighted_average(ds, var, season = None, months = None, 
                            trend = False, trend_period = slice('1950','2020')):
    '''''
    This function calculates the mean weighted (cos(lat)) of a specific variable over the years in an xarray dataset.
    
    Parameters:
    ----------
    ds: xarray Dataset
        The dataset containing the variable.
    var: str
        The name of the variable to calculate the mean for.
     season: str
         The season for which to calculate the mean ('Annual', 'DJF', 'MAM', 'JJA', 'SON').
    months: list
        Specific months to include in the calculation, overrides season if provided.
    
    Returns:
    ----------
    ds_years: xarray DataArray
            The dataset with the variable's mean calculated over the years.
    '''''
     # If specific months are provided, select only those months from the dataset
    if season:
        ds = ds.sel(time=ds['time.month'].isin(season))
          
    dates = pd.to_datetime(ds['time'].values)
    years = np.array([date.year for date in dates])
    ds_w_years = ds.assign_coords(year=('time', years))
    ds_years = ds_w_years[var].groupby('year').mean(dim=['time'], skipna=True)
    #add weights
    weights = np.cos(np.deg2rad(ds_years['lat']))
    ds_years_weighted = ds_years.weighted(weights).mean(dim=['lat', 'lon'], skipna=True)
    
    if trend == True:
        # Perform linear regression
        results = sp.stats.linregress(ds_years_weighted.sel(year = trend_period).year, 
                                      ds_years_weighted.sel(year = trend_period).values)
        return ds_years_weighted, results
    else:    
        return ds_years_weighted
    
def monthly_weighted_average(ds, var, mode = None, diff = None, baseline_period=None, period = None, ds_GWLs = None):
    '''
    This function calculates the mean weighted (cos(lat)) of a specific variable over the months in an xarray dataset.
    
    Parameters:
    ----------
    ds: xarray Dataset
        The dataset containing the variable.
    var: str
        The name of the variable to calculate the mean for.
    mode: (str, optional): 
        The calculation mode, can be "climatology" or "change". Default is None.
    diff: str, optional
        Type of difference to calculate ("abs" for absolute, "rel" for relative). Default is None.
    baseline_period: slice, optional
        The time period to be considered as the baseline for calculating the mean. Default is None.
    period: slice, optional
        The time period to calculate the mean for in "change" mode. Default is None.
    ds_GWLs: xarray Dataset, optional
        The dataset containing the variable grouped by month. Default is None.
    
    Returns:
    ----------
    ds_months_weighted: xarray DataArray
        The dataset with the variable's mean calculated over the months, with weights applied.
    '''
    if mode == "climatology":
        # Extracting month information from the time dimension
        dates = pd.to_datetime(ds['time'].values)
        months = np.array([date.month for date in dates])
        # Assigning month coordinates to the dataset
        ds_w_months = ds.assign_coords(month=('time', months))
        
        # Calculating mean for each month
        ds_months = ds_w_months[var].groupby('month').mean(dim='time', skipna=True)
    
        weights = np.cos(np.deg2rad(ds_months['lat']))
        ds_months_weighted = ds_months.weighted(weights).mean(dim=['lat', 'lon'], skipna=True)
    if mode == "change":
        # Extracting month information from the time dimension
        dates = pd.to_datetime(ds['time'].values)
        months = np.array([date.month for date in dates])
        # Assigning month coordinates to the dataset
        ds_w_months = ds.assign_coords(month=('time', months))
        if ds_GWLs is not None:
            weights_GWLs = np.cos(np.deg2rad(ds_GWLs['lat']))
            ds_months_weighted_period = ds_GWLs[var].weighted(weights_GWLs).mean(
                dim=['lat', 'lon'], skipna=True)
        else:
            # Calculating mean for each month
            ds_months = ds_w_months[var].sel(time = period).groupby('month').mean(
                dim='time', skipna=True)
            weights = np.cos(np.deg2rad(ds_months['lat']))
            
            # Adding weights based on latitude
            ds_months_weighted_period = ds_months.weighted(weights).mean(
                dim=['lat', 'lon'], skipna=True)
                
        # Calculating mean for each month within the baseline period   
        ds_months_baseline = ds_w_months[var].sel(time = baseline_period).groupby('month').mean(dim='time', skipna=True)
        weights = np.cos(np.deg2rad(ds_months_baseline['lat']))
        ds_months_weighted_baseline = ds_months_baseline.weighted(weights).mean(
            dim=['lat', 'lon'], skipna=True)

        # Calculating the difference if specified
        if diff== 'abs':
            ds_months_weighted=ds_months_weighted_period - ds_months_weighted_baseline
        elif diff== 'rel':
            ds_months_weighted=(ds_months_weighted_period - ds_months_weighted_baseline)/abs(ds_months_weighted_baseline) * 100
    return ds_months_weighted

def seasonal_stripes(ds,var, model):
    """
    Reshape the dataset into a matrix with months and years as dimensions.

    Parameters
    ----------
    ds : xr.Dataset
        The filtered ds
    var : str
        The name of the variable
    model : str
        The model used for the calculations.
    Returns
    -------
    xr.DataArray
        DataArray reshaped with months and years as dimensions.
    """
    if model in ["ERA5", "ERA5-Land", "E-OBS", "ORAS5"]:# models that don't have member 
        mean=ds[var]
    else:
        mean=ds[var].mean(dim=['member'])
    
    # Extract year and month from the time coordinate
    mean = mean.assign_coords(year=('time', mean['time.year'].values))
    mean = mean.assign_coords(month=('time', mean['time.month'].values))
    
    # Group by year and month and take the mean for each group
    reshaped = mean.groupby('year').apply(lambda x: x.groupby('month').mean(dim='time'))

    #add weights
    weights = np.cos(np.deg2rad(reshaped['lat']))
    reshaped_weighted = reshaped.weighted(weights).mean(dim=['lat', 'lon'], skipna=True)

    return reshaped_weighted

def significance_trends(ds, var, season = None, trend_period = slice('1950','2020')):
    """
    This function calculates and returns p-values for linear regression trends
    of a variable (`var`) across a specified time period (`trend_period`) for
    each latitude-longitude point in an xarray.Dataset (`ds`).
    
    Args:
      ds : xarray.Dataset 
      The input dataset containing the variable and time dimension.
      var: str
      The name of the variable in the dataset for which to calculate trends.
      trend_period :  list
      A list of two integers representing the start and end year
          of the trend period (inclusive).
    
    Returns:
      list: A list of dictionaries, each containing:
          - 'lat': Latitude value of the data point.
          - 'lon': Longitude value of the data point.
          - 'pvalue': p-value from the linear regression for this point.
    """
    if season:
        ds = ds.sel(time=ds['time.month'].isin(season))
        
    dates = pd.to_datetime(ds['time'].values)
    years = np.array([date.year for date in dates])
    ds_w_years = ds.assign_coords(year=('time', years))
    ds_years = ds_w_years.groupby('year').mean(dim=['time'], skipna=True)
    ds_years = ds_years.sel(year= trend_period)
    results = []  # Initialize a list to store results
    
    # Initialize a list to store significance points
    slope_matrix = np.full((len(ds.lat.values), len(ds.lon.values)), np.nan)
    pvalue_matrix = np.full((len(ds.lat.values), len(ds.lon.values)), np.nan)
    
    for lat_idx, lat in enumerate(ds.lat.values):
        for lon_idx, lon in enumerate(ds.lon.values):
            sub_ds = ds_years.sel(lat=lat, lon=lon)
            # Ensure the lengths match between variable and time
            result = sp.stats.linregress(sub_ds.year, sub_ds[var].values)  # Perform linear regression
            # store results
            pvalue_matrix[lat_idx, lon_idx] = result.pvalue
            slope_matrix[lat_idx, lon_idx] = result.slope

    ds['slope'] = (["lat", "lon"], slope_matrix)
    ds['pvalue'] = (["lat", "lon"], pvalue_matrix)
    
    return ds

def Pelt(series, time = None, model = 'l1', pen=5):
    """
    Detect the first year where the mean becomes non-stationary using PELT.
    
    Parameters:
    series : 1D array
        Time series values (e.g., annual or monthly aggregated).
    time : 1D array
        Corresponding datetime64 or numeric years.
    pen : float
        Linear penalty parameter for PELT (controls sensitivity to breakpoints).
    
    Returns:
    int or np.nan
        First year where a change in the mean is detected, or np.nan if none found.
    """
    # Convert time to numeric years if it is datetime64
    if np.issubdtype(time.dtype, np.datetime64):
        years = pd.DatetimeIndex(time).year.values
    else:
        years = np.array(time)
    
    # Skip all-NaN or too-short series
    if len([v for v in series if v is not None and not math.isnan(v)]) < 3:
        return -9999
    
    # Apply PELT to detect breakpoints in the mean
    algo = rpt.Pelt(model=model).fit(series.reshape(-1,1))
    bps = algo.predict(pen=pen)
    
    # If a breakpoint is detected, return the corresponding year
    if len(bps) > 1:
        return years[bps[0]-1]
    
    # Return NaN if no non-stationary year is found
    return np.nan
    
def apply_Pelt_xarray(da, model='l1', pen=5):
    """
    Apply find_nonstationary_year_1d to an xarray.DataArray along 'time'.
    Returns a DataArray with the first non-stationary year.
    """
    def wrapper(series, time):
        series = np.asarray(series)
        time = np.asarray(time)
        return Pelt(series, time, model=model, pen=pen)
    
    result = xr.apply_ufunc(
        wrapper,
        da,
        da['time'].values,
        input_core_dims=[['time'], ['time']],
        output_core_dims=[[]],  # scalar output
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float]
    )
    
    # Preserve spatial dimensions (everything except time)
    coords = {dim: da.coords[dim] for dim in da.dims if dim != 'time'}
    dims = list(coords.keys())
    
    return xr.DataArray(result, coords=coords, dims=dims, name='nonstationary_year')

def snht_pyhomogeneity(series, time=None, alpha=0.05):
    """
    Apply the Standard Normal Homogeneity Test (SNHT) using the pyhomogeneity package.
    """
    # Convert to pandas Series with optional time index
    if time is not None:
        series_pd = pd.Series(series, index=pd.Index(time))
    else:
        series_pd = pd.Series(series)

    # Skip all-NaN or too-short series
    if series_pd.dropna().size < 2:
        return {
            'snht_stat': np.nan,
            'break_year': np.nan,
            'significant': np.nan,
            'critical_value': np.nan,
            'p_value': np.nan
        }

    # Run SNHT test
    result = hg.snht_test(series_pd, alpha=alpha, sim=1000)
    
    snht_stat = float(getattr(result, 'T', np.nan))
    break_index = getattr(result, 'cp', None)

    # Determine break_year
    break_year = np.nan
    if break_index is not None:
        break_time = pd.to_datetime(break_index)
        break_year = break_time.year

    return {
        'snht_stat': snht_stat,
        'break_year': break_year,
        'significant': bool(getattr(result, 'h', False)),
        'p_value': float(getattr(result, 'p', np.nan))
    }

def apply_snht_to_xarray(da, alpha=0.05):
    """
    Apply snht_pyhomogeneity along the 'time' dimension of an xarray.DataArray.
    Returns an xarray.Dataset with variables:
    snht_stat, break_year, significant, critical_value.

    Handles NaNs and Dask arrays automatically.

    Parameters
    ----------
    da : xarray.DataArray
        Input DataArray with 'time' dimension.
    alpha : float, optional
        Significance level for SNHT.

    Returns
    -------
    xarray.Dataset
        Dataset containing SNHT results along all spatial dimensions.
    """
    # Extract the time coordinate as numpy array
    time_values = da['time'].values

    # Wrapper for vectorization
    def wrapper(series):
        res = snht_pyhomogeneity(series, time=time_values, alpha=alpha)
        return res['snht_stat'], res['break_year'], res['significant'], res['p_value']

    # Apply SNHT along 'time' dimension using xarray vectorization
    snht_result = xr.apply_ufunc(
        wrapper,
        da,
        input_core_dims=[['time']],
        output_core_dims=[[], [], [], []],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float, float, bool, float],
        keep_attrs=True
    )

    # Preserve non-time coordinates
    coords = {dim: da.coords[dim] for dim in da.dims if dim != 'time'}
    dims = list(coords.keys())

    # Build output Dataset
    ds = xr.Dataset({
        'snht_stat': xr.DataArray(snht_result[0], coords=coords, dims=dims),
        'break_year': xr.DataArray(snht_result[1], coords=coords, dims=dims),
        'significant': xr.DataArray(snht_result[2], coords=coords, dims=dims),
        'p_value': xr.DataArray(snht_result[3], coords=coords, dims=dims)
    })

    return ds

def plot_break_year(snht_spei6, pelt_spei6, decades):
    # Create cmap
    n_colors = len(decades)
    base_cmap = plt.get_cmap('gnuplot2', n_colors-1)
    colors = base_cmap(np.arange(n_colors-1))  
    last_color = np.array([[1.0, 1.0, 0.8, 1.0]])
    colors = np.vstack([colors, last_color])
    cmap_custom = mcolors.ListedColormap(colors)
    boundaries = decades
    norm = mcolors.BoundaryNorm(boundaries=boundaries, ncolors=len(colors))
    norm = mcolors.BoundaryNorm(boundaries=boundaries, ncolors=cmap_custom.N)

    # Create subplot with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True,
                             subplot_kw={'projection': ccrs.PlateCarree()})
    
    # SNHT test plot (no colorbar)
    da = snht_spei6.copy()
    lon2d, lat2d = np.meshgrid(da['lon'].values, da['lat'].values)
    data = da.values
    mask_real = da['break_year'].where(da['significant'])
    pcm = axes[0].pcolormesh(
        da['lon'].values, 
        da['lat'].values, 
        mask_real,
        cmap=cmap_custom,
        norm=norm,
        transform=ccrs.PlateCarree()
    )
    
    mask_nodata = ~np.isnan(da['break_year'].where(da['significant']==False))
    axes[0].contourf(
        lon2d, lat2d, mask_nodata,
        levels=[0, 0.5, 1],   # divide False y True
        colors='none',        # sin color de relleno
        hatches=['', '///////'],
        transform=ccrs.PlateCarree()
    )
    
    axes[0].set_title(f'SNHT (significant only, alpha={alpha})')
    axes[0].coastlines()
    
    # PELT test plot (no colorbar)
    da = pelt_spei6.copy()
    lon2d, lat2d = np.meshgrid(da['lon'].values, da['lat'].values)
    data = da.values
    mask_real = (data != -9999) & (~np.isnan(data))
    pcm = axes[1].pcolormesh(
        da['lon'].values, da['lat'].values, np.where(mask_real, data, np.nan),
        cmap=cmap_custom,
        norm=norm,
        transform=ccrs.PlateCarree()
    )
    
    mask_nodata = np.isnan(data)
    axes[1].contourf(
        lon2d, lat2d, mask_nodata,
        levels=[0, 0.5, 1],   # divide False y True
        colors='none',        # sin color de relleno
        hatches=['', '///////'],
        transform=ccrs.PlateCarree()
    )
    
    axes[1].set_title('PELT')
    axes[1].coastlines()
    
    # Add a single shared colorbar for both plots
    # Use the last plotted image as mappable
    # Colorbar compartida discreta
    cbar_ax = fig.add_axes([0.25, 0.1, 0.5, 0.04])  # posición de la colorbar
    cbar = fig.colorbar(
        mappable=pcm, 
        cax=cbar_ax, 
        orientation='horizontal',
        ticks=decades,
    )
    cbar.set_label('Break Year (decade)')
    plt.tight_layout()
    plt.show()
    #fig.savefig("SNHT_PELT_SPI6.pdf")

def identify_droughts_vectorized(
    ds,
    drought_start_threshold=-1,
    drought_end_threshold=0,
    min_duration=2
):
    """
    Drought is defined following [Spinoni et al., (2020)](https://doi.org/10.1175/JCLI-D-19-0084.1) 
    as a period where SPEI6 < -1 for ≥2 months, extended until SPEI6 > 0
    Applies this logic to every spatial grid cell in an xarray Dataset, returning a new 'drought_spei6' 
    variable with NaN for non-drought periods.
    Vectorized function to identify drought events in a SPEI6 time series.
    Only values that are part of a valid drought event are included.
    """
    # Initialize output
    drought_series = ds.copy()
    drought_series[:] = np.nan

    # Find where SPEI6 is below the start threshold
    below_start = ds < drought_start_threshold

    # Find runs of at least min_duration consecutive months below the start threshold
    runs = np.zeros_like(ds, dtype=bool)
    for i in range(len(ds) - min_duration + 1):
        if np.all(below_start[i:i + min_duration]):
            runs[i:i + min_duration] = True

    # Extend runs until SPEI6 turns positive
    for i in range(len(ds)):
        if runs[i]:
            j = i + 1
            while j < len(ds) and ds[j] <= drought_end_threshold:
                runs[j] = True
                j += 1

    # Only include values that are part of a valid drought event
    drought_series = np.where(runs, ds, np.nan)
    # Find the start and end of each drought event
    starts = np.where((~runs[:-1]) & runs[1:])[0] + 1
    if runs[0]:
        starts = np.insert(starts, 0, 0)

    # Assign unique IDs to each drought event
    drought_ids = np.full_like(ds, np.nan, dtype=float)
    for drought_id, start in enumerate(starts, start=1):
        end = start
        while end < len(ds) and runs[end]:
            drought_ids[end] = drought_id
            end += 1
    return drought_series,drought_ids
    
def apply_drought_identification(ds, spei_var="spei6"):
    """
    Apply drought identification to every point in an xarray Dataset.

    Parameters:
    - ds (xarray.Dataset): Dataset containing SPEI6 data.
    - spei_var (str): Name of the SPEI6 variable in the dataset.

    Returns:
    xarray.Dataset: Dataset with a new variable for drought periods.
    """
    # Apply the function to every point
    results = xr.apply_ufunc(
        identify_droughts_vectorized,
        ds[spei_var],
        input_core_dims=[["time"]],
        output_core_dims=[["time"], ["time"]],
        vectorize=True,
        kwargs={
            "drought_start_threshold": -1,
            "drought_end_threshold": 0,
            "min_duration": 2,
        },
    )
    ds["drought_spei6"] = results[0]
    ds["drought_ids"] = results[1]
    return ds

def plot_drought_metrics_comparison(ds_list, name_list, city):

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ds_list[0].plot(ax=ax, label=name_list[0], linestyle='--')
    ds_list[1].plot(ax=ax, label=name_list[1], linestyle='--', marker='+')
    
    ax.set_ylabel('Drought vs SPEI')
    ax.axhline(y=-1, color='r', linestyle='--', label='Drought Threshold (-1)')
    ax.grid()
    ax.legend()
    
    plt.xlabel('Date')
    plt.title(f'Drought Series {city}')
    plt.tight_layout()
    plt.show()

def count_drought_events_per_decade(drought_id):
    """
    Count unique drought events in 10-year periods (1951–1960, 1961–1970, ...),
    using xarray.resample and labeling at the end of each block.

    Parameters:
    - drought_id (xarray.DataArray): DataArray of drought IDs (NaN for non-drought periods).

    Returns:
    - xarray.DataArray: Number of unique drought events per 10-year interval,
                        labeled at the end of each block.
    """

    def count_unique_ids(x):
        # Remove NaNs and count unique drought IDs
        x = x[~np.isnan(x)]
        return len(np.unique(x))

    # Resample every 10 years, closing the interval on the right and labeling at the end
    droughts_per_10y = drought_id.resample(time='10A', label='right', closed='right').map(
        lambda da: xr.apply_ufunc(
            count_unique_ids,
            da,
            input_core_dims=[["time"]],
            vectorize=True,
            dask="parallelized",
            output_dtypes=[int],
        )
    )

    # Adjust the time coordinate to show the final year of each block
    droughts_per_10y['time'] = [
        np.datetime64(f"{t.dt.year.item():04d}-01-01") for t in droughts_per_10y['time']
    ]

    # Name the resulting DataArray
    droughts_per_10y.name = "drought_count"
    return droughts_per_10y

def count_droughts(drought_da):
    """
    Count the number of distinct drought events for every spatial point in the dataset.

    Parameters:
    - drought_da (xarray.DataArray): Drought DataArray with dimensions (time, lat, lon).

    Returns:
    - xarray.DataArray: Number of distinct drought events for each spatial point.
    """
    def count_droughts_1d(drought_series):
        """
        Count distinct drought events (contiguous non-NaN segments) in a 1D drought series.
        """
        values = drought_series
        if len(values) == 0:
            return np.nan
        # Boolean mask: True where drought exists
        is_drought = ~np.isnan(values)
        if not np.any(is_drought):
            return np.nan
        # Count transitions from False → True (start of a drought event)
        drought_count = np.sum((~is_drought[:-1]) & (is_drought[1:])) + (1 if is_drought[0] else 0)
        return int(drought_count) if drought_count > 0 else np.nan

    # Apply the function along the time dimension
    drought_counts = xr.apply_ufunc(
        count_droughts_1d,
        drought_da,
        input_core_dims=[["time"]],
        output_core_dims=[[]],
        vectorize=True,
    ).rename("drought_count")

    return drought_counts

def calculate_event_severities(series):
    """
    Calculate the severity per drought event (DS) for a given period.

    Parameters:
    - drought_da (xarray.DataArray): Drought DataArray for the period.

    Returns:
    - xarray.DataArray: Average severity per drought event (DS) for each spatial point.
    """
    # Extract drought events
    droughts = []
    in_drought = False
    current_drought = []

    for value in series:
        if not np.isnan(value):
            current_drought.append(value)
            in_drought = True
        else:
            if in_drought:
                droughts.append(current_drought)
                current_drought = []
                in_drought = False
    # Add the last drought if it ends at the last timestep
    if in_drought:
        droughts.append(current_drought)

    # Calculate severity for each drought event
    severities = []
    for drought in droughts:
        severity = np.sum(np.abs(drought))
        severities.append(severity)

    return severities

def calculate_average_severity(drought_da):
    """
    Calculate the average severity per drought event (DS) for a given period.

    Parameters:
    - drought_da (xarray.DataArray): Drought DataArray for the period.

    Returns:
    - xarray.DataArray: Average severity per drought event (DS) for each spatial point.
    """
    def calculate_ds_1d(series):
        severities=calculate_event_severities(series)
        ds = np.mean(severities) if severities else np.nan
        return ds

    # Apply the function along the time dimension
    ds_values = xr.apply_ufunc(
        calculate_ds_1d,
        drought_da,
        input_core_dims=[["time"]],
        output_core_dims=[[]],
        vectorize=True,
    ).rename("drought_severity")

    return ds_values
    
def calculate_peak_events(ref_drought_da, fut_drought_da):
    """
    Calculate the number of peak drought events in a future period that are more severe than the most severe event in a reference period.

    Parameters:
    - ref_drought_da (xarray.DataArray): Drought DataArray for the reference period (e.g., 1981-2010).
    - fut_drought_da (xarray.DataArray): Drought DataArray for the future period (e.g., 2071-2100).

    Returns:
    - xarray.DataArray: Number of peak events (PK) for each spatial point.
    """
    def calculate_pk_1d(ref_series, fut_series):
        # Extract drought events and severities for reference and future periods
        ref_severities = calculate_event_severities(ref_series)
        fut_severities = calculate_event_severities(fut_series)

        # Most severe event in the reference period
        max_ref_severity = np.max(ref_severities) if ref_severities else np.nan
        # If there are no reference drought events, return NaN
        if np.isnan(max_ref_severity):
            return np.nan, np.nan
        # Count how many future drought events are more severe than the reference period's most severe event
        pk_count = sum(1 for severity in fut_severities if severity > max_ref_severity)

        return pk_count,max_ref_severity

    # Apply the function along the time dimension
    results = xr.apply_ufunc(
        calculate_pk_1d,
        ref_drought_da,
        fut_drought_da,
        input_core_dims=[["time"], ["time"]],
        output_core_dims=[[], []],  # Two outputs, each with no core dimension
        vectorize=True,
        exclude_dims=set(("time",)),  # Exclude the time dimension from alignment
    )
    pk_events = results[0].rename("peak_events")
    ref_max_severity = results[1].rename("ref_max_severity")
    return pk_events, ref_max_severity

def to_per_decade(da, start, end):
    """
    Convert a DataArray to per-decade values for a specified period.
    
    Parameters
    ----------
    da : xarray.DataArray
        DataArray with a 'time' coordinate.
    start : str
        Start date as 'YYYY-MM-DD'.
    end : str
        End date as 'YYYY-MM-DD'.
        
    Returns
    -------
    per_decade : xarray.DataArray
        The variable normalized per decade over the given period.
    """
    # Extract years from the dates
    start_year = int(start.split('-')[0])
    end_year = int(end.split('-')[0])
    
    # Number of years and decades
    n_years = end_year - start_year + 1
    n_decades = n_years / 10.0
    
    # Normalize per decade
    per_decade = da/ n_decades
    
    return per_decade

def plot_drought_maps(
    data_list,
    titles,
    cbar_labels,
    v_scales,
    nrows=2,
    figsize=(14, 12),
    cmap=['hot_r', 'coolwarm']
):
    """
    Plot a series of drought severity maps with colorbars.

    Parameters:
    - data_list: List of xarray DataArrays or similar 2D arrays to plot.
    - titles: List of titles for each subplot.
    - cbar_labels: List of labels for each colorbar.
    - v_scales: List of [min, max] value scales for each plot.
    - nrows: Number of rows in the figure (default: 2).
    - figsize: Figure size (default: (14, 12)).
    - cmap: Colormap to use (default: 'RdYlBu_r').
    """
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(nrows, 2, width_ratios=[100, 1], wspace=0.01, hspace=0.1)

    for i in range(nrows):
        ax = fig.add_subplot(gs[i, 0], projection=ccrs.PlateCarree())
        data = data_list[i]
        v_scale = v_scales[i]

        mesh = ax.pcolormesh(
            data.lon, data.lat, data,
            transform=ccrs.PlateCarree(),
            cmap=cmap[i],
            vmin=v_scale[0], vmax=v_scale[1],
        )

        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.set_title(titles[i], fontsize=12)

        cax = fig.add_subplot(gs[i, 1])
        cbar = fig.colorbar(mesh, cax=cax, orientation='vertical')
        cbar.set_label(cbar_labels[i])

    plt.show()


