def get_years(dataset):
    """
    :param dataset: opened netCDF4 file
    :return: years_found_set: set of all years found in the dataset
             desired_years_set: set of years from 2010 to 2019 from dataset
    """
    df = dataset.to_dataframe()
    dates = df['time_bnds']  # select time column from dataset
    desired_years_set = set()
    years_found_set = set()
    desired_years = ['2010', '2011', '2012', '2013', '2014',
                     '2015', '2016', '2017', '2018', '2019']
    for i in dates:
        year = i.strftime('%Y')  # get just the year; ignore days/months/hours/minutes/seconds
        years_found_set.add(year)
        if year in desired_years:
            desired_years_set.add(year)
    return years_found_set, desired_years_set
