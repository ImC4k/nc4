from nc4 import load_nc4, get_nc4_precipitation_stat, download_nc4, download_all_nc4_by_url_file
from gis import load_gis, save_gis, augment_gis_lat_lon
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
        iso_times.append(iso_time)

    # download nc4 files
    for iso_time in iso_times:
        download_nc4(iso_time)

def main():
    #  update augment file name here
    location = 'philippines'
    input_gis_file_path = f'./GIS/augmented-{location}.csv'
    output_gis_file_path = f'./GIS/precipitation-{location}.csv'

    gis = load_gis(input_gis_file_path, ['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME', 'LAT', 'LON', 'LAT_MIN', 'LAT_MAX', 'LON_MIN', 'LON_MAX'], 'SID')
    download_all_nc4_for_gis(gis) # make subsequent calls faster


    # for each row, add precipitation max, mean and min, save to a new csv
    df = pd.DataFrame()
    
    for index, row in gis.iterrows(): # variables are positional, do not remove unused ones
        iso_time = row['ISO_TIME']
        if iso_time == '<Null>':
            continue
        
        day, month, year = iso_time.split('/') # variables are positional, do not remove unused ones
        if int(year) < 2000: # lacking nc4 data
            continue
        if row['SID'] != '2000185N15117': # disable this checking to run for all SIDs
            continue

        data = load_nc4(row['ISO_TIME'])
        precipitation_stat = get_nc4_precipitation_stat(data, row['LAT_MIN'], row['LAT_MAX'], row['LON_MIN'], row['LON_MAX'])
        # print(precipitation_stat)
        row['PRECIPITATION_MAX'] = precipitation_stat["max"]
        row['PRECIPITATION_MEAN'] = precipitation_stat["mean"]
        # row['PRECIPITATION_MIN'] = precipitation_stat["min"]

        df = pd.concat([df, row.to_frame().T], ignore_index=True)

    save_gis(df, output_gis_file_path)



if __name__ == "__main__":
    main()