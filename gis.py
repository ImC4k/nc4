import pandas

def load_gis(csv_file_path):
    usecols = ['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME', 'LAT', 'LON']
    df = pandas.read_csv(csv_file_path, index_col='SID', usecols=usecols)
    return df

def augment_gis(csv_file_path, augment_file_path):
    csv = load_gis(csv_file_path)
    # create new data frame by grouping by SID, SEASON, NUMBER, NAME and ISO_TIME, take average of LAT and LON respectively
    df = csv.groupby(['SID', 'SEASON', 'NUMBER', 'NAME', 'ISO_TIME'])[['LAT', 'LON']].mean().reset_index()
    # augment with LAT_MIN, LAT_MAX, round to nearest 0.1
    df['LAT_MIN'] = df['LAT'].apply(lambda x: round(round(x, 1) + 0.05 - 1, 2))
    df['LAT_MAX'] = df['LAT'].apply(lambda x: round(round(x, 1) - 0.05 + 1, 2))
    # augment with LON_MIN, LON_MAX
    df['LON_MIN'] = df['LON'].apply(lambda x: round(round(x, 1) + 0.05 - 1, 2))
    df['LON_MAX'] = df['LON'].apply(lambda x: round(round(x, 1) - 0.05 + 1, 2))
    # save as csv
    df.to_csv(augment_file_path, index=False)
    return df