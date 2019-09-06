import calendar

import numpy as np
from netCDF4 import Dataset as NetCDF
from scipy import interpolate

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


print(interp_precip_in_point())
