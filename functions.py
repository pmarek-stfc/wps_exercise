import xarray as xr
from SortedSet.sorted_set import SortedSet
from itertools import combinations


def get_years(dataset):
    """
    :param dataset: netCDF4 file
    :return: None: if the range of years in the dataset doesn't include years 2010 to 2019
             years_found_set: sorted set of all years found in the dataset
             desired_years_set: sorted set of years from 2010 to 2019 from dataset
    """
    open_dataset = xr.open_dataset(dataset)
    first_year_in_dataset = open_dataset.variables['time_bnds'][0].data[0].strftime('%Y')
    if first_year_in_dataset > '2019':
        return None
    else:
        df = open_dataset.to_dataframe()
        dates = df['time_bnds']
        desired_years_set = set()
        years_found_set = set()
        desired_years = ['2010', '2011', '2012', '2013', '2014',
                         '2015', '2016', '2017', '2018', '2019']

        for i in dates:
            year = i.strftime('%Y')
            years_found_set.add(year)
            if year in desired_years:
                desired_years_set.add(year)
        return SortedSet(years_found_set), SortedSet(desired_years_set)


def couple_subset(files):
    """ return list of tuples of all subsets of length couple """
    couple = 2
    return list(combinations(files, couple))


def open_mfdatasets(files_to_open):
    """

    :param files_to_open: found netCDF4 files
    :return: set of correct datasets
    """
    correct_dataset_couples = []
    for combination in files_to_open:
        try:
            dataset = xr.open_mfdataset(combination)
            if dataset:
                correct_dataset_couples.append(combination)
        except ValueError:
            continue
    correct_dataset = set()
    for elements in correct_dataset_couples:
        correct_dataset.update(elements)
    return correct_dataset

