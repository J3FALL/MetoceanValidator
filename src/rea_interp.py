import calendar
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

    return nc_file[var_name][:]


def interp_precip_in_point(year, rea_name='ncep', path_to_rea='../reanalysis/ncep_1964-1979/arctic_precip_y1964.nc'):
    precip = extracted_precip(path_to_rea=path_to_rea, rea_name=rea_name)

    station_xy = [[171, 75], [180, 75], [174, 63]]
    station = 0
    prec_data = precip[:, station_xy[station][1], station_xy[station][0]]

    prec_data = np.sum(prec_data.reshape(-1, 4), axis=1)

    prec_data = ((prec_data * 3600 / 4
                  * 24
                  ) ** 1.5) * 0.3853

    steps = days_in_year(year) * 24
    int_prec_data = interpolate.interp1d(range(1, steps, 24), prec_data, fill_value='extrapolate')

    resulted = []
    for time in range(steps):
        resulted.append(int_prec_data(time) / 24)

    return resulted


def interp_precip_field(year=1964, rea_name='ncep', path='../reanalysis/ncep_1965-1979/arctic_precip_y1964.nc'):
    precip = extracted_precip(path_to_rea=path,
                              rea_name=rea_name)

    precip_transposed = np.transpose(precip, (1, 2, 0))

    precip_daily = np.sum(np.reshape(precip_transposed, (452, 406, -1, 4)), axis=-1)
    precip_daily = np.power(precip_daily * 3600 / 4 * 24, 1.5) * 0.3853

    days = days_in_year(year)

    resulted = np.zeros((452, 406, days * 24))

    for day in tqdm(range(days - 1)):
        field_from = precip_daily[:, :, day]
        field_to = precip_daily[:, :, day + 1]

        for time in range(0, 24):
            resulted[:, :, (day * 24) + time] = linear_interpolated_field(field_from, field_to, time) / 24

    return resulted


def linear_interpolated_field(field_from, field_to, time):
    interp_value = (field_to - field_from) * time / 23 + field_from

    return interp_value


def save_interp_precip(prev_file_path, fixed_file_path, interp_precip, time):
    copyfile(prev_file_path, fixed_file_path)

    nc_file = NetCDF(fixed_file_path, mode='r+')
    var_name = FIELDS_BY_REA_NAME['ncep']
    nc_file[var_name][:] = interp_precip
    nc_file['time'][:] = time
    nc_file.close()


def fix_precip_attributes(path):
    nc_file = NetCDF(path, mode='r+')
    nc_file.history = ''
    nc_file.variables['precip'].long_name = 'Daily Precipitation Rate at surface'
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


def interp_all_ncep():
    rea = 'ncep'
    for year in range(1965, 1980):
        path_to_rea = f'../reanalysis/ncep_1964-1979/arctic_precip_y{year}.nc'
        print(f'File: {path_to_rea}')
        expected_ts = interp_precip_in_point(year=year, rea_name=rea,
                                             path_to_rea=path_to_rea)
        actual_full = interp_precip_field(year=year, rea_name=rea,
                                          path=path_to_rea)

        print(f'prev_shape = {actual_full.shape}')
        precip_resulted = np.transpose(actual_full, (2, 0, 1))
        print(f'resulted_shape = {precip_resulted.shape}')

        actual_ts = actual_full[75, 171, :]
        plot_precip_in_point(expected_ts, actual_ts, figure_name=f'../{year}.png')

        fixed_file_path = f'../reanalysis/ncep_1964-1979/precip_interp_y{year}.nc'

        time = hourly_time(path_to_rea, year)
        save_interp_precip(path_to_rea, fixed_file_path, precip_resulted, time)
        fix_precip_attributes(fixed_file_path)


if __name__ == '__main__':
    interp_all_ncep()
