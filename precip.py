import pandas
from netCDF4 import Dataset # typical python libaray for open netcdf file 
import numpy as np # typical python libaray for array operation 
import matplotlib.pyplot as plt  # typical python libaray for plotting
import cartopy.crs as ccrs # typical python libaray for plotting coastlines, maps
import cartopy.feature as cfeature


file_path = '../IMERG/'  #open country 1 csv file

i = len(file)
sid = 0
all_lat = []
all_lon = []

for i in range(len(file)-1): #exclude header row
    row = i+1
    sid_current = file[row[0]]
    if sid_current != sid:
        sid = sid_current
        date = file[row[4]]
        line = [row]
    else:
        if file[row[4]] == date:
            line.append(row)
        else:
            if len(line) == 1:
                continue
            else:
                for j in range(len(line)):
                    lat = file(line[j][6])
                    lat = round(lat*2) / 2
                    all_lat.append(lat)
                    lon = file(line[j][7])
                    lon = round(lon*2) / 2
                    all_lon.append(lon)
                average_lat = np.mean(all_lat)
                average_lon = np.mean(all_lon)
                adjusted_date =     #change date format to yyyymmdd
                #open link to txt file and open link with adjusted_date
                ncfile_path = '../IMERG/'
                data = Dataset(ncfile_path)
                
                date = file[row[4]]
                line = [row]



