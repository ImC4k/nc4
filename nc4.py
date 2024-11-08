import requests
import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

download_directory = './IMERG'

username = ''
password = ''

"""
    Downloads a netCDF4 file from NASA's IMERG data server based on the given ISO date string (in 'dd/mm/yyyy' format).

    Parameters
    ----------
    iso_date : str
        The ISO date string in 'dd/mm/yyyy' format.

    Returns
    -------
    None

    Notes
    -----
    This function requires the `requests` library to be installed and the
    `username` and `password` variables to be set in the calling scope.
    """
def download_nc4(iso_date):
    day, month, year = iso_date.split('/')
    padded_day = day.zfill(2)
    padded_month = month.zfill(2)
    formatted_date = f'{year}{padded_month}{padded_day}'
    print(f'Downloading nc4 data for {year}-{padded_month}-{padded_day}')

    # create IMERG directory if it doesn't exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    url = f'https://data.gesdisc.earthdata.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07/{year}/{padded_month}/3B-DAY.MS.MRG.3IMERG.{year}{padded_month}{padded_day}-S000000-E235959.V07B.nc4'
    print(f'url is {url}')

    # assuming variables `username`, `password` and `url` are set...
    with requests.Session() as session:
        session.auth = (username, password)
        r1 = session.request('get', url)
        r = session.get(r1.url, auth=(username, password))
        if r.ok:
            # save file to disk
            with open(f'{download_directory}/{formatted_date}.nc4', 'wb') as f:
                f.write(r.content)
            print(f'Downloaded nc4 data for {year}-{padded_month}-{padded_day}')
        else:
            print(f'Error downloading nc4 data for {year}-{padded_month}-{padded_day}: {r.reason}')
            raise Exception(f'Error downloading nc4 data for {year}-{padded_month}-{padded_day}: {r.reason}')



def load_nc4(iso_date):
    day, month, year = iso_date.split('/')
    padded_day = day.zfill(2)
    padded_month = month.zfill(2)
    formatted_date = f'{year}{padded_month}{padded_day}'

    file_path = f'{download_directory}/{formatted_date}.nc4'
    if os.path.exists(file_path):
        return Dataset(file_path)
    else:
        download_nc4(iso_date)
        return Dataset(file_path)

def get_nc4_precipitation_stat(dataset, min_lat, max_lat, min_lon, max_lon):
    standardize = lambda x: round(x * 10)
    standardized_min_lat = standardize(min_lat)
    standardized_max_lat = standardize(max_lat)
    standardized_min_lon = standardize(min_lon)
    standardized_max_lon = standardize(max_lon)
    precipitation = dataset.variables['precipitation'][0]
    lat = dataset.variables['lat'][standardized_min_lat:standardized_max_lat]
    lon = dataset.variables['lon'][standardized_min_lon:standardized_max_lon]
    lon_2d, lat_2d = np.meshgrid(lon, lat)

    # precipitation_transposed = np.transpose(precipitation)
    precipitation_ranged = precipitation[standardized_min_lon:standardized_max_lon, standardized_min_lat:standardized_max_lat]
    # plot this range
    fig, ax = plt.subplots(figsize=(10, 5))
    # Create contour plot
    precipitation_levels = np.arange(0,200,2)
    precip_contour=ax.contourf(lon_2d, lat_2d, precipitation_ranged , levels=precipitation_levels, cmap='jet',extend='max')
    # Add color bar
    plt.show()

    # precipitation_ranged = precipitation_transposed[standardize(min_lon):standardize(max_lon), standardize(min_lat):standardize(max_lat)]
    return { "mean": np.ma.mean(precipitation_ranged), "max": np.ma.max(precipitation), "min": np.ma.min(precipitation_ranged) }