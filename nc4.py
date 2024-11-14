import requests
import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

download_directory = './IMERG'

username = ''
password = ''

def download_nc4_by_url(url, output_path):
    # create IMERG directory if it doesn't exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    with requests.Session() as session:
        session.auth = (username, password)
        r1 = session.request('get', url)
        r = session.get(r1.url, auth=(username, password))
        if r.ok:
            # save file to disk
            with open(f'{download_directory}/{output_path}', 'wb') as f:
                f.write(r.content)
            print(f'Downloaded nc4 data for {output_path}')
        else:
            print(f'Error downloading nc4 data for {output_path}: {r.reason}')
            raise Exception(f'Error downloading nc4 data for {output_path}: {r.reason}')

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
    output_path = f'{formatted_date}.nc4'
    print(f'Downloading nc4 data for {output_path}')


    url = f'https://data.gesdisc.earthdata.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07/{year}/{padded_month}/3B-DAY.MS.MRG.3IMERG.{year}{padded_month}{padded_day}-S000000-E235959.V07B.nc4'
    print(f'url is {url}')

    # assuming variables `username`, `password` and `url` are set...
    download_nc4_by_url(url, output_path)

def download_all_nc4_by_url_file(url_file_path):
    
    urls = []
    with open(url_file_path, 'r') as file:
        for line in file:
            urls.append(line.strip())

    for url in urls:
        last_slash = url.split('/')[-1]
        dot_split_4 = last_slash.split('.')[4]
        output_path = dot_split_4.split('-')[0]
        output_path = f'{output_path}.nc4'
        if os.path.exists(f'{download_directory}/{output_path}'):
            print(f'Skipping download of {output_path} because it already exists')
            continue
        download_nc4_by_url(url, output_path)

def load_nc4(iso_date):
    day, month, year = iso_date.split('/')
    padded_day = day.zfill(2)
    padded_month = month.zfill(2)
    formatted_date = f'{year}{padded_month}{padded_day}'

    file_path = f'{download_directory}/{formatted_date}.nc4'
    if not os.path.exists(file_path):
        download_nc4(iso_date)
    return Dataset(file_path)

def get_nc4_precipitation_stat(dataset, min_lat, max_lat, min_lon, max_lon):
    precipitation = dataset.variables['precipitation'][0]
    lon_size, lat_size = precipitation.shape
    standardize_lon = lambda x: round(round(x, 1) * 10 + lon_size / 2) # offset for negative longitudes
    standardize_lat = lambda x: round(round(x, 1) * 10 + lat_size / 2) # offset for negative latitudes
    standardized_min_lat = standardize_lat(min_lat) - 1
    standardized_max_lat = standardize_lat(max_lat) + 1
    standardized_min_lon = standardize_lon(min_lon) - 1
    standardized_max_lon = standardize_lon(max_lon) + 1

    precipitation_ranged = precipitation[standardized_min_lon:standardized_max_lon, standardized_min_lat:standardized_max_lat]
    return { "mean": np.ma.mean(precipitation_ranged), "max": np.ma.max(precipitation_ranged), "min": np.ma.min(precipitation_ranged), "count": np.ma.count(precipitation_ranged) }