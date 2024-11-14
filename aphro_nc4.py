import requests
import os
from netCDF4 import Dataset
import numpy as np

download_directory = './IMERG'

def load_nc4(iso_date):
    day, month, year = iso_date.split('/')

    file_path = f'{download_directory}/APHRO_MA_025deg_V1101.{year}.nc'
    if not os.path.exists(file_path):
        raise Exception(f'File {file_path} does not exist, please download it first or implement a download function')
    return Dataset(file_path)

def round_to_nearest_interval(value, step, start):
    return start + round((value - start) / step) * step

def to_index(value, step, start):
    translated = round_to_nearest_interval(value, step, start)
    return round((translated - start) / step)

def to_value(index, step, start):
    return start + index * step

def get_nc4_precipitation_stat(dataset, min_lat, max_lat, min_lon, max_lon, long_variable, lat_variable, target_variable, time_dimension):
    target = dataset.variables[target_variable][time_dimension]
    longitude = dataset.variables[long_variable]
    longitude_step = longitude[1] - longitude[0]
    latitude = dataset.variables[lat_variable]
    latitude_step = latitude[1] - latitude[0]
    standardized_min_lat = to_index(min_lat, latitude_step, latitude[0]) - 1
    standardized_max_lat = to_index(max_lat, latitude_step, latitude[0]) + 1
    standardized_min_lon = to_index(min_lon, longitude_step, longitude[0]) - 1
    standardized_max_lon = to_index(max_lon, longitude_step, longitude[0]) + 1

    precipitation_ranged = target[standardized_min_lon:standardized_max_lon, standardized_min_lat:standardized_max_lat]

    max_position = np.ma.argmax(precipitation_ranged)
    max_lon_index = max_position // precipitation_ranged.shape[1]
    max_lat_index = max_position % precipitation_ranged.shape[1]
    max_coordinate = (to_value(max_lon_index + standardized_min_lon, longitude_step, longitude[0]), to_value(max_lat_index + standardized_min_lat, latitude_step, latitude[0]))
    return {
        "mean": np.ma.mean(precipitation_ranged),
        "max": np.ma.max(precipitation_ranged),
        "min": np.ma.min(precipitation_ranged),
        "count": np.ma.count(precipitation_ranged),
        "lat_min_index": standardized_min_lat,
        "lat_max_index": standardized_max_lat,
        "lon_min_index": standardized_min_lon,
        "lon_max_index": standardized_max_lon,
        "max_coordinate": max_coordinate
        }