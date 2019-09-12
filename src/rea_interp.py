import calendar
import os
from shutil import copyfile

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset as NetCDF
from scipy import interpolate
from tqdm import tqdm

FIELDS_BY_REA_NAME = {
    'dfs': 'precip',
    'ncep': 'precip',
    'era': 'var228'
}


def days_in_year(year):
    return 366 if calendar.isleap(year) else 365


def extracted_precip(path_to_rea, rea_name):
    nc_file = NetCDF(path_to_rea, mode='r')

    var_name = FIELDS_BY_REA_NAME[rea_name]

    precip = nc_file[var_name][:]
    if rea_name is 'era':
        precip[precip < 0.0] = 0.0

    return precip


def interp_precip_in_point(year, rea_name='ncep', path_to_rea='../reanalysis/ncep_1964-1979/arctic_precip_y1964.nc'):
    precip = extracted_precip(path_to_rea=path_to_rea, rea_name=rea_name)

    station_xy = [[171, 75], [180, 75], [174, 63]]
    station = 0
    prec_data = precip[:, station_xy[station][1], station_xy[station][0]]

    if rea_name is 'ncep':
        prec_data = np.sum(prec_data.reshape(-1, 4), axis=1)

        prec_data = ((prec_data * 3600 / 4
                      * 24
                      ) ** 1.5) * 0.3853
    elif rea_name is 'dfs':
        prec_data = ((prec_data * 3600 * 24) ** 1.5) * 0.3853
    elif rea_name is 'era':
        prec_data = np.sum(prec_data.reshape(-1, 2), axis=1)
        prec_data = ((prec_data * 3600 * 24 / 24) ** 1.5) * 0.3853

    steps = days_in_year(year) * 24
    int_prec_data = interpolate.interp1d(range(1, steps, 24), prec_data, fill_value='extrapolate')

    resulted = []
    for time in range(steps):
        resulted.append(int_prec_data(time) / 24)

    return resulted


def interp_precip_field(year=1964, rea_name='ncep', path='../reanalysis/ncep_1965-1979/arctic_precip_y1964.nc'):
    precip = extracted_precip(path_to_rea=path,
                              rea_name=rea_name)

    precip_daily = prepared_precip_daily(precip=precip, rea_name=rea_name)

    days = days_in_year(year)

    resulted = np.zeros((452, 406, days * 24))

    for day in tqdm(range(days - 1)):
        field_from = precip_daily[:, :, day]
        field_to = precip_daily[:, :, day + 1]

        for time in range(0, 24):
            resulted[:, :, (day * 24) + time] = linear_interpolated_field(field_from, field_to, time) / 24

    return resulted


def prepared_precip_daily(precip, rea_name):
    precip_transposed = np.transpose(precip, (1, 2, 0))

    if rea_name is 'ncep':
        precip_daily = np.sum(np.reshape(precip_transposed, (452, 406, -1, 4)), axis=-1)
        precip_daily = np.power(precip_daily * 3600 / 4 * 24, 1.5) * 0.3853
        return precip_daily
    elif rea_name is 'dfs':
        precip_daily = np.power(precip_transposed * 3600 * 24, 1.5) * 0.3853
        return precip_daily
    elif rea_name is 'era':
        precip_daily = np.sum(np.reshape(precip_transposed, (452, 406, -1, 2)), axis=-1)
        precip_daily = np.power(precip_daily * 3600 * 24 / 24, 1.5) * 0.3853

        return precip_daily


def linear_interpolated_field(field_from, field_to, time):
    interp_value = (field_to - field_from) * time / 23 + field_from

    return interp_value


def save_interp_precip(prev_file_path, fixed_file_path, rea_name, interp_precip, time):
    copyfile(prev_file_path, fixed_file_path)

    nc_file = NetCDF(fixed_file_path, mode='r+')
    var_name = FIELDS_BY_REA_NAME[rea_name]
    nc_file[var_name][:] = interp_precip
    nc_file['time'][:] = time
    nc_file.close()


def fix_precip_attributes(path):
    nc_file = NetCDF(path, mode='r+')
    nc_file.history = ''
    nc_file.variables['precip'].long_name = 'Daily Precipitation Rate at surface'

    if 'Identification' in nc_file.ncattrs():
        nc_file.Identification = ''
    if 'Documentation' in nc_file.ncattrs():
        nc_file.Documentation = ''
    if 'About' in nc_file.ncattrs():
        nc_file.About = ''

    nc_file.close()


def plot_precip_in_point(expected_ts, actual_ts, figure_name='comparison.png'):
    time = [hour for hour in range(len(expected_ts))]

    plt.figure()
    plt.plot(time, expected_ts, label='expected')
    plt.plot(time, actual_ts, label='actual')
    plt.legend()

    plt.savefig(figure_name)


def hourly_time(path_to_rea, year):
    nc_file = NetCDF(path_to_rea, mode='r')
    first_hour = int(nc_file['time'][:][0])
    last_hour = first_hour + days_in_year(year) * 24
    nc_file.close()

    time = [time_step for time_step in range(first_hour, last_hour)]

    return np.asarray(time)


def interp_ncep_precip(year):
    path_to_rea = f'../reanalysis/ncep_1964-1979/arctic_precip_y{year}.nc'
    path_to_fixed_file = f'../reanalysis/ncep_1964-1979/precip_interp_y{year}.nc'

    interp_reanalysis(rea_name='ncep', year=year, path_to_rea=path_to_rea, path_to_fixed_file=path_to_fixed_file)


def interp_dfs_precip(year):
    path_to_rea = f'../reanalysis/dfs_1980-2015/dfs_precipf_y{year}.nc'
    path_to_fixed_file = f'../reanalysis/dfs_1980-2015/precip_interp_y{year}.nc'
    interp_reanalysis(rea_name='dfs', year=year, path_to_rea=path_to_rea, path_to_fixed_file=path_to_fixed_file)


def interp_era_precip(year):
    path_to_rea = f'../reanalysis/era_2016-2017/era-prec-y{year}.nc'
    path_to_fixed_file = f'../reanalysis/era_2016-2017/precip_interp_y{year}.nc'
    rea_to_copy = f'../reanalysis/arctic_precip_y1975.nc'
    interp_reanalysis(rea_name='era', year=year, path_to_rea=path_to_rea, path_to_fixed_file=path_to_fixed_file,
                      rea_to_copy=rea_to_copy)


def interp_reanalysis(rea_name, year, path_to_rea, path_to_fixed_file, **kwargs):
    print(f'File: {path_to_rea}')
    expected_ts = interp_precip_in_point(year=year, rea_name=rea_name,
                                         path_to_rea=path_to_rea)
    actual_full = interp_precip_field(year=year, rea_name=rea_name,
                                      path=path_to_rea)

    print(f'prev_shape = {actual_full.shape}')
    precip_resulted = np.transpose(actual_full, (2, 0, 1))
    print(f'resulted_shape = {precip_resulted.shape}')

    actual_ts = actual_full[75, 171, :]
    plot_precip_in_point(expected_ts, actual_ts, figure_name=f'../{year}.png')

    time = hourly_time(path_to_rea, year)

    if rea_name is 'era':
        if 'rea_to_copy' in kwargs.keys():
            rea_to_copy = kwargs['rea_to_copy']
            save_interp_precip(rea_to_copy, path_to_fixed_file, 'ncep', precip_resulted, time)
        else:
            raise ValueError(f'rea_name is {rea_name}, but rea_to_copy was not found')
    else:
        save_interp_precip(path_to_rea, path_to_fixed_file, rea_name, precip_resulted, time)
    fix_precip_attributes(path_to_fixed_file)


def interp_all_ncep():
    year_from = 1973
    year_to = 1979
    for year in range(year_from, year_to + 1):
        interp_ncep_precip(year)


def interp_all_dfs():
    year_from, year_to = 2014, 2015
    for year in range(year_from, year_to + 1):
        interp_dfs_precip(year)


def test_era_misses():
    nc_file = NetCDF('../reanalysis/era_2016-2017/era-prec-y2016.nc')
    station_coords = [171, 75]

    prec_at_point = nc_file.variables['var228'][:][75, 171, :]
    print(prec_at_point)
    nc_file.close()


def daily_average(path_to_interp_files):
    for year in range(2016, 2018):
        file_path = os.path.join(path_to_interp_files, f'precip_interp_y{year}.nc')
        nc_file = NetCDF(file_path)
        prec_at_point = nc_file.variables['precip'][:][75, 171, :]
        nc_file.close()
        avg_precip = np.average(prec_at_point)
        total_precip = np.sum(prec_at_point)

        del prec_at_point
        print(f'year: {year}; avg_precip: {avg_precip}; total: {total_precip}')


if __name__ == '__main__':
    # interp_ncep_precip(1975)
    interp_era_precip(2016)
    interp_era_precip(2017)
    daily_average('../reanalysis/era_2016-2017')
