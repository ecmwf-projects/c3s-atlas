import os
from pathlib import Path
import zipfile
import xarray as xr
import numpy as np
import datetime
import glob
import json

# Get current directory
c_path = Path(__file__)
c_path_c3s_atlas = c_path.parents[1]

def extract_zip_and_delete(zip_path):
    """
    Function to extract zip files and rename .nc file
    
    Parameters
    ----------
    zip_path (pathlib.Path): path to the downloaded zip files
    """
    with zipfile.ZipFile(zip_path , 'r') as zip_ref:
        names = zip_ref.namelist()
        temporal_files = [
            f"{zip_path.parent}/{name}" for name in names if name.split(".")[-1] == "nc"
        ]
        zip_ref.extractall(zip_path.parent)
        for name in names:
            print(name)
            if name.split(".")[-1] == "nc":
                os.rename(f"{zip_path.parent}/{name}", 
                          zip_path.with_name(zip_path.name.replace('.zip', '.nc'))
                         )
            else:
                os.remove(f"{zip_path.parent}/{name}") 

    os.remove(zip_path)

def get_ds_to_fill(variable: str, target: xr.Dataset, reference: xr.Dataset):
    """
    Create an empty dataset which will be filled with the bias adjusted data.

    Parameters
    ----------
    variable (str): variable name
    dataset (xarray.dataset): dataset reference to create the new dataset to fill,
    this dataset must be the experiment/future dataset

    Returns
    -------
    ds_bias (xarray.Dataset): empty dataset with the same dimensions and
    coordinates that the reference dataset provided
    """
    ds_bias = xr.Dataset(
        data_vars={
            f"{variable}": (
                ["time", "lon", "lat"],
                np.zeros(
                    shape=(
                        len(target.time.values),
                        len(reference.lon.values),
                        len(reference.lat.values),
                    )
                ),
            ),
        },
        coords=dict(
            time=(["time"], target.time.values),
            lon=(["lon"], reference.lon.values),
            lat=(["lat"], reference.lat.values),
        ),
    )
    return ds_bias

def load_IAMD(
    root, 
    project, 
    var, 
    scenario = None):
    """
    Load data from the Interactive Atlas Monthly Dataset. If climate change projections (CMIP5/6 or CORDEX) are required then 
    emission and historical scenarios are loaded and concatenated. 
    If historical scenarios is request the highest emission escenario is loaded to complet until the last complete year.
    """
    if project in ['CMIP5','CMIP6', 'CORDEX-EUR-11', 'CORDEX-CORE']:
        if scenario == 'historical':
            if project in ['CMIP5', 'CORDEX-EUR-11', 'CORDEX-CORE']:
                scenario = 'rcp85'
            else:
                scenario = 'ssp585'

        file_sce = glob.glob(str(root / f"{project}/{scenario}/{var}_*.nc"))
        file_hist = glob.glob(str(root / f"{project}/historical/{var}_*.nc"))
        ds_hist = xr.open_dataset(file_hist[0])
        ds_sce = xr.open_dataset(file_sce[0])
        mem_inters = np.intersect1d(ds_hist.member_id.values, ds_sce.member_id.values)
        ds_hist = ds_hist.isel(member = np.in1d(ds_hist.member_id.values, mem_inters))
        ds_sce = ds_sce.isel(member = np.in1d(ds_sce.member_id.values, mem_inters))
        ds = xr.concat([ds_hist, ds_sce], dim = 'time')
        if scenario == 'historical':
            today = datetime.date.today()
            year = str(today.year -1)
            target_date = f"{year}-12-31"
            # Convert the target date to a datetime object
            target_date = pd.to_datetime(target_date)
            # Select time until the target date
            ds = ds.sel(time=ds['time'] <= target_date)
    else:
        file = glob.glob(str(root / f"{project}/{var}_*.nc"))
        ds = xr.open_dataset(file[0])

    return ds

def get_attribute(attrs, name):
    """
    Function to get the name of a variable from the attrs dictionary.

    Parameters:
    -----------
    attrs : dict
        Dictionary containing the attributes.
    name : str
        Name of the attribute you are looking for.

    Returns:
    --------
    str
        Name of the variable.
    """
    # Open and read the JSON file
    with open(f"{c_path_c3s_atlas}/auxiliar/settings.json", 'r') as file:
        settings = json.load(file)
    
    return settings.get('variable', {}).get(name, {}).get('name')

def season_get_name(season):
    '''
    Returns the name of the season or month based on the input.

    Parameters:
    -----------
    season : int, str, or list of int
        If int, represents either the month number or the season index.
        If str, represents the season abbreviation (e.g., 'DJF', 'MAM', 'JJA', 'SON').
        If list of int, represents a list of month numbers.

    Returns:
    --------
    str
        The name of the season or month, or list of names.
    '''

    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    if isinstance(season, int):
        # If the input is an integer, assume it represents a month number
        return month_names[season - 1]

    elif isinstance(season, list):
        # If list, map each element and join with commas
        return ', '.join([month_names[m - 1] for m in season])  # Use list comprehension
    else:
        # If the input is a string, map the season names accordingly
        season_mapping = {
            'DJF': 'Winter',
            'MAM': 'Spring',
            'JJA': 'Summer',
            'SON': 'Autumn'
        }
        return season_mapping.get(season.upper(), 'Unknown')

def count_years(period):
    start_year = int(period.start)
    end_year = int(period.stop)
    return end_year - start_year + 1

def plot_month(ax, ds, var, month, title, cmap, vmin = None, vmax = None):
    ds[var].sel(time=(ds['time.month'] == month)).plot(ax=ax, cmap = cmap, vmin = vmin, vmax = vmax)
    ax.set_title(title, fontsize = 16)
    ax.coastlines()
