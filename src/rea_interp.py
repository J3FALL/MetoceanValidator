import calendar

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


def interp_precip_in_point():
    precip = extracted_precip(path_to_rea='../reanalysis/ncep_1965-1979/arctic_precip_y1964.nc',
                              rea_name='ncep')

    station_xy = [[171, 75], [180, 75], [174, 63]]
    station = 0
    prec_data = precip[:, station_xy[station][1], station_xy[station][0]]

    prec_data = np.sum(prec_data.reshape(-1, 4), axis=1)

    prec_data = ((prec_data * 3600 / 4
                  * 24
                  ) ** 1.5) * 0.3853

    steps = days_in_year(1964) * 24
    int_prec_data = interpolate.interp1d(range(1, steps, 24), prec_data, fill_value='extrapolate')

    resulted = []
    for time in range(steps):
        resulted.append(int_prec_data(time) / 24)

    return resulted


def interp_precip_field(year=1964):
    precip = extracted_precip(path_to_rea='../reanalysis/ncep_1965-1979/arctic_precip_y1964.nc',
                              rea_name='ncep')

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


def plot_precip_in_point(expected_ts, actual_ts):
    time = [hour for hour in range(len(expected_ts))]

    plt.figure()
    plt.plot(time, expected_ts, label='expected')
    plt.plot(time, actual_ts, label='actual')
    plt.legend()

    plt.savefig('comparison.png')


if __name__ == '__main__':
    expected_ts = interp_precip_in_point()
    actual_full = interp_precip_field()

    actual_ts = actual_full[75, 171, :]

    plot_precip_in_point(expected_ts, actual_ts)
