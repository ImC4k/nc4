import pandas

# columns ['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME', 'LAT', 'LON']
# index 'SID'
def load_gis(csv_file_path, columns, index):
    df = pandas.read_csv(csv_file_path, usecols=columns)
    return df

def save_gis(df, csv_file_path):
    df.to_csv(csv_file_path, index=False)

# TODO refactor me to be more generic
def augment_gis_lat_lon(csv_file_path, augment_file_path):
    csv = load_gis(csv_file_path)
    # create new data frame by grouping by SID, SEASON, NUMBER, NAME and ISO_TIME, take average of LAT and LON respectively
    df = csv.groupby(['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME'])[['LAT', 'LON']].mean().reset_index()
    # augment with LAT_MIN, LAT_MAX, round to nearest 0.1
    min_fx = lambda x: round(round(x, 1) - 0.95, 2)
    max_fx = lambda x: round(round(x, 1) + 0.95, 2)
    df['LAT_MIN'] = df['LAT'].apply(min_fx)
    df['LAT_MAX'] = df['LAT'].apply(max_fx)
    # augment with LON_MIN, LON_MAX
    df['LON_MIN'] = df['LON'].apply(min_fx)
    df['LON_MAX'] = df['LON'].apply(max_fx)
    # save as csv
    save_gis(df, augment_file_path)
    return df