import xarray as xr
# from itertools import combinations


def _get_years(dataset):
    """
        Check if a dataset contains a specific range of years
        :param dataset: a NetCDF4 file
        :return: a file containing years 2010-2020
    """
    REQ_YEARS = set([int(_) for _ in range(2010, 2020)])
    ds = xr.open_dataset(dataset)
    years = set([int(_) for _ in ds.time.dt.year])

    if REQ_YEARS.issubset(years):
        return dataset


def get_years(fpaths):
    """
        :param fpaths: path to files
        :return: list of files containing specific range of years
    """
    files_in_range = []

    for fpath in fpaths:
        processed_file = _get_years(fpath)
        if processed_file is not None:
            files_in_range.append(processed_file)
    return files_in_range

# def couple_subset(files):
#     """ Returns all possible couples of files """
#     couple = 2
#     return list(combinations(files, couple))


def open_mfdatasets(files_to_open):
    """
        :param files_to_open: netCDF4 files
        :return: opened netCDF datasets using `open_mfdataset`
    """
    try:
        # ALWAYS USE combine='by_coords' with open_mfdataset
        with xr.open_mfdataset(files_to_open, combine='by_coords') as ds:
            return ds
    except Exception as e:
        return e
