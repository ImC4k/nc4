from aphro_nc4 import load_nc4, get_nc4_precipitation_stat
from gis import load_gis, save_gis
from location import get_coordinate_pairs, get_region_coordinate_pairs
import pandas as pd
from datetime import date

def get_number_of_date_in_year(iso_date):
    day, month, year = iso_date.split('/')
    d = date(int(year), int(month), int(day))
    return d.timetuple().tm_yday

def process_location(location):
    #  update augment file name here
    input_gis_file_path = f'./GIS/augmented-{location}.csv'
    output_gis_file_path = f'./GIS/precipitation-{location}.csv'

    gis = load_gis(input_gis_file_path, ['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME', 'LAT', 'LON', 'LAT_MIN', 'LAT_MAX', 'LON_MIN', 'LON_MAX'], 'SID')
    # coordinate_pairs = get_coordinate_pairs(location)
    regions = get_region_coordinate_pairs(location)
    # download_all_nc4_for_gis(gis) # make subsequent calls faster


    # for each row, add precipitation max, mean and min, save to a new csv
    df = pd.DataFrame()
    
    for index, gis_row in gis.iterrows(): # variables are positional, do not remove unused ones
        iso_time = gis_row['ISO_TIME']
        if iso_time == '<Null>':
            continue
        
        day, month, year = iso_time.split('/') # variables are positional, do not remove unused ones
        if int(year) < 1998 or int(year) > 2023: # lacking nc4 data
            continue
        if gis_row['SID'] != '2004231N09147': # disable this checking to run for all SIDs
            continue

        # iso_date = gis_row['ISO_TIME']
        iso_date = "10/1/1951"
        
        data = load_nc4(iso_date)
        time_dimension = get_number_of_date_in_year(iso_date) - 1
        for region in regions:
            row = gis_row.copy()
            location_max = 0
            location_data_count = 0
            location_mean = 0
            region_name = region["region_name"]
            coordinate_pairs = region["coordinate_pairs"]
            for coordinate_pair in coordinate_pairs:
                min_coordinate, max_coordinate = coordinate_pair
                min_lat, min_lon = min_coordinate
                max_lat, max_lon = max_coordinate
                precipitation_stat = get_nc4_precipitation_stat(data, min_lat, max_lat, min_lon, max_lon, 'longitude', 'latitude', 'precip', time_dimension)
                location_max = max(location_max, precipitation_stat["max"])
                old_location_data_count = location_data_count
                location_data_count += precipitation_stat["count"]
                location_mean = (location_mean * old_location_data_count + precipitation_stat["mean"] * precipitation_stat["count"]) / location_data_count 
            # print(precipitation_stat)
            row['LAT_MIN'] = min_lat
            row['LAT_MAX'] = max_lat
            row['LON_MIN'] = min_lon
            row['LON_MAX'] = max_lon
            row['PRECIPITATION_MAX'] = location_max
            row['PRECIPITATION_MEAN'] = location_mean
            row['LAT_MIN_INDEX'] = precipitation_stat["lat_min_index"]
            row['LAT_MAX_INDEX'] = precipitation_stat["lat_max_index"]
            row['LON_MIN_INDEX'] = precipitation_stat["lon_min_index"]
            row['LON_MAX_INDEX'] = precipitation_stat["lon_max_index"]
            row['REGION_NAME'] = region_name
            

            df = pd.concat([df, row.to_frame().T], ignore_index=True)

    save_gis(df, output_gis_file_path)

def main():
    # locations = ['cambodia', 'guangdong', 'hongkong', 'laos', 'malaysia', 'myanmar', 'philippines', 'taiwan', 'thailand', 'vietnam']
    locations = ['hongkong']
    for location in locations:
        process_location(location)


if __name__ == "__main__":
    main()