from nc4 import load_nc4, get_nc4_precipitation_stat, download_nc4, download_all_nc4_by_url_file
from gis import load_gis, save_gis, augment_gis_lat_lon
from location import get_coordinate_pairs
import pandas as pd

def download_all_nc4():
    download_all_nc4_by_url_file('./data_url.txt')


def download_all_nc4_for_gis(gis):
    # all iso_time
    iso_times = []
    for index, row in gis.iterrows():
        iso_time = row['ISO_TIME']
        if iso_time == '<Null>':
            continue
        day, month, year = iso_time.split('/') # variables are positional, do not remove unused ones
        if int(year) < 1998 or int(year) > 2023: # lacking nc4 data
            continue
        iso_times.append(iso_time)

    # download nc4 files
    for iso_time in iso_times:
        download_nc4(iso_time)

def process_location(location):
    #  update augment file name here
    input_gis_file_path = f'./GIS/augmented-{location}.csv'
    output_gis_file_path = f'./GIS/precipitation-{location}.csv'

    gis = load_gis(input_gis_file_path, ['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME', 'LAT', 'LON', 'LAT_MIN', 'LAT_MAX', 'LON_MIN', 'LON_MAX'], 'SID')
    coordinate_pairs = get_coordinate_pairs(location)
    # download_all_nc4_for_gis(gis) # make subsequent calls faster


    # for each row, add precipitation max, mean and min, save to a new csv
    df = pd.DataFrame()
    
    for index, row in gis.iterrows(): # variables are positional, do not remove unused ones
        iso_time = row['ISO_TIME']
        if iso_time == '<Null>':
            continue
        
        day, month, year = iso_time.split('/') # variables are positional, do not remove unused ones
        if int(year) < 1998 or int(year) > 2023: # lacking nc4 data
            continue
        if row['SID'] != '2004231N09147': # disable this checking to run for all SIDs
            continue

        data = load_nc4(row['ISO_TIME'])
        location_max = 0
        location_data_count = 0
        location_mean = 0
        for coordinate_pair in coordinate_pairs:
            min_coordinate, max_coordinate = coordinate_pair
            min_lat, min_lon = min_coordinate
            max_lat, max_lon = max_coordinate
            precipitation_stat = get_nc4_precipitation_stat(data, min_lat, max_lat, min_lon, max_lon)
            location_max = max(location_max, precipitation_stat["max"])
            old_location_data_count = location_data_count
            location_data_count += precipitation_stat["count"]
            location_mean = (location_mean * old_location_data_count + precipitation_stat["mean"] * precipitation_stat["count"]) / location_data_count 
        # print(precipitation_stat)
        row['PRECIPITATION_MAX'] = location_max
        row['PRECIPITATION_MEAN'] = location_mean

        del row["LAT_MIN"]
        del row["LAT_MAX"]
        del row["LON_MIN"]
        del row["LON_MAX"]


        df = pd.concat([df, row.to_frame().T], ignore_index=True)

    save_gis(df, output_gis_file_path)

def main():
    # locations = ['cambodia', 'guangdong', 'hongkong', 'laos', 'malaysia', 'myanmar', 'philippines', 'taiwan', 'thailand', 'vietnam']
    locations = ['hongkong']
    for location in locations:
        process_location(location)


if __name__ == "__main__":
    main()