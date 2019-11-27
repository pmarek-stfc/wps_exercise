import xarray as xr
from SortedSet.sorted_set import SortedSet
from itertools import combinations


def _get_first_year(ds):
    # first_year = ds.variables['time_bnds'][0].data[0].strftime('%Y')
    first_year = int(ds.time.dt.year[0])
    return first_year

def _check_for_years(ds):
    """
    Get through all years in a dataset
    :param ds: a netCDF4 file
    :return: set of years (should return years 2010 to 2019)
    """
    # convert to Pandas data frame
    df = ds.to_dataframe()
    dates = df['time_bnds']
    dates = dates[0::12]
    desired_years_set = set()
    # years_found_set = set()

    for i in dates:
        year = i.strftime('%Y')
        print(year)
        # years_found_set.add(year)
        if 2009 < int(year) < 2020:
            desired_years_set.add(year)
    return desired_years_set


def get_years(dataset):
    """
        :param dataset: netCDF4 file or files
        :return: None: if the dataset does not include years 2010 to 2019
                 valid_files: a list of files which contain years 2010 to 2019
    """
    valid_files = []
    if isinstance(dataset, str):
        with xr.open_dataset(dataset) as ds:
            year = _get_first_year(ds)
            print(f'working with: {dataset}, first year is: {year}')
            if year > 2019:
                return None
            desired_years = _check_for_years(ds)
            if len(desired_years) == 10:
                valid_files.append(dataset)


    else:
        for file in dataset:
            with xr.open_dataset(file) as ds:
                year = _get_first_year(ds)
                print(f'working with: {file}, first year is: {year}')
                if year > 2019:
                    continue
                desired_years = _check_for_years(ds)
                if len(desired_years) == 10:
                    valid_files.append(file)
    return valid_files


def couple_subset(files):
    """ Returns all possible couples of files """
    couple = 2
    return list(combinations(files, couple))


def open_mfdatasets(files_to_open):
    """
        Test if a couple of data sets can be aggregated together
        and add them into a set if so
        :param files_to_open: found netCDF4 files
        :return: opened netCDF data sets using `open_mfdataset`
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
    return xr.open_mfdataset(correct_dataset)
