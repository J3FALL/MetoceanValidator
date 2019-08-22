import datetime
import re
from shutil import copyfile

from netCDF4 import Dataset as NetCDF

file_name_patterns = [
    'ARCTIC_1h_ice_grid_TUV_(\\d{8})-(\\d{8}).nc',
    'ARCTIC_1h_T_grid_T_(\\d{8})-(\\d{8}).nc',
    'ARCTIC_1h_UV_grid_UV_(\\d{8})-(\\d{8}).nc'
]


def fix_missed_variables(directory, file_to_fix, previous_file):
    copyfile(f'{directory}/{previous_file}', f'{directory}/fixed_{file_to_fix}')
    file_with_errors = NetCDF(f'{directory}/{file_to_fix}', mode='r')
    fixed_file = NetCDF(f'{directory}/fixed_{file_to_fix}', mode='r+')

    for var_name in file_with_errors.variables:
        if var_name not in fixed_file.variables:
            print(f'Variable {var_name} not in previous file')
        elif fixed_file[var_name].shape != fixed_file[var_name].shape:
            print(f'Variable {var_name} with incompatible shape:'
                  f' expected - {fixed_file[var_name].shape}, actual - {file_with_errors[var_name].shape}')
        else:
            fixed_file[var_name][:] = file_with_errors[var_name][:]

    file_with_errors.close()
    fixed_file.close()


def fix_time_variables(directory, file_to_fix, previous_file, time_dif=86400.0):
    copyfile(f'{directory}/{previous_file}', f'{directory}/fixed_{file_to_fix}')
    fixed_file = NetCDF(f'{directory}/fixed_{file_to_fix}', mode='r+')

    for time_var in ['time_counter', 'time_instant', 'time_counter_bounds', 'time_counter_bounds']:
        if time_var not in fixed_file.variables:
            print(f'Variable {time_var} is not in {file_to_fix}')
        else:
            fixed_file[time_var][:] += time_dif

    fixed_file.close()


def fix_corrupted_file(directory, file_to_fix, previous_file):
    fix_time_variables(directory, file_to_fix, previous_file)


def fix_missed_day(directory, ice, tracers, currents):
    date_raw = extracted_date_by_pattern(ice)
    date = datetime.datetime.strptime(date_raw, '%Y%m%d')

    next_day = date + datetime.timedelta(days=1)
    next_day_raw = next_day.strftime('%Y%m%d')

    ice_fixed_file = f'ARCTIC_1h_ice_grid_TUV_{next_day_raw}-{next_day_raw}.nc'
    fix_corrupted_file(directory, ice_fixed_file, ice)

    tracers_fixed_file = f'ARCTIC_1h_T_grid_T_{next_day_raw}-{next_day_raw}.nc'
    fix_corrupted_file(directory, tracers_fixed_file, tracers)

    currents_fixed_file = f'ARCTIC_1h_UV_grid_UV_{next_day_raw}-{next_day_raw}.nc'
    fix_corrupted_file(directory, currents_fixed_file, currents)


def extracted_date_by_pattern(file_name):
    for pattern in file_name_patterns:
        matches = re.search(pattern, file_name)
        if matches is None:
            continue
        if len(matches.groups()) > 0:
            return matches.groups()[0]


def test_files_time_dif_correct(directory, first_file, second_file):
    first = NetCDF(f'{directory}/{first_file}')
    second = NetCDF(f'{directory}/{second_file}')

    time_var = 'time_counter'

    print(second[time_var][:][0] - first[time_var][:][0])


# storage_path = '/home/hpc-rosneft/nfs/110_31/NEMO-ARCT/coarse_grid/'
year = 1988

storage_path = '../fixed_files'

prev_file = 'ARCTIC_1h_T_grid_T_19900709-19900709.nc'
file_to_fix = 'ARCTIC_1h_T_grid_T_19900710-19900710.nc'


def fixes_example():
    fix_missed_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix,
                         previous_file=prev_file)

    fix_time_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix, previous_file=prev_file)

    test_files_time_dif_correct(directory=f'{storage_path}/{year}',
                                first_file='ARCTIC_1h_T_grid_T_20140929-20140929.nc',
                                second_file='fixed_ARCTIC_1h_T_grid_T_20140930-20140930.nc')

    fix_corrupted_file(directory=f'{storage_path}/{year}',
                       file_to_fix=file_to_fix, previous_file=prev_file)


if __name__ == '__main__':
    fix_missed_day(directory=f'{storage_path}/{year}',
                   ice='ARCTIC_1h_ice_grid_TUV_19880228-19880228.nc',
                   tracers='ARCTIC_1h_T_grid_T_19880228-19880228.nc',
                   currents='ARCTIC_1h_UV_grid_UV_19880228-19880228.nc')
