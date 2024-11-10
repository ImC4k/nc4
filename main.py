from nc4 import load_nc4, get_nc4_precipitation_stat, download_all_nc4_by_url_file
from gis import load_gis, augment_gis

def main():
    # gis = augment_gis('./GIS/philippines.csv', './GIS/augmented-philippines.csv')
    
    # for index, row in gis.iterrows(): # variables are positional, do not remove unused ones
    #     iso_time = row['ISO_TIME']
    #     if iso_time == '<Null>':
    #         continue
        
    #     day, month, year = iso_time.split('/') # variables are positional, do not remove unused ones
    #     if int(year) < 2000: # lacking nc4 data
    #         continue
    #     if row['SID'] != '2004319N10134': # disable this checking to run for all SIDs
    #         continue

    #     data = load_nc4(row['ISO_TIME'])
    #     precipitation_stat = get_nc4_precipitation_stat(data, row['LAT_MIN'], row['LAT_MAX'], row['LON_MIN'], row['LON_MAX'])
    #     print(precipitation_stat)
    #     row['PRECIPITATION_MAX'] = precipitation_stat["max"]
    #     row['PRECIPITATION_MEAN'] = precipitation_stat["mean"]
    #     row['PRECIPITATION_MIN'] = precipitation_stat["min"]

    # gis.to_csv('./GIS/precipitation-philippines.csv', index=False)
    
    # data = load_nc4('4/7/2000')

    # precipitation_stat = get_nc4_precipitation_stat(data, 16.95,18.85,119.35,121.25)

    # print(precipitation_stat)

    # print('a')

    download_all_nc4_by_url_file('./data_url.txt')



if __name__ == "__main__":
    main()