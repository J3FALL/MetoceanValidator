from shutil import copyfile

from netCDF4 import Dataset as NetCDF


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
        fixed_file[time_var][:] += time_dif

    fixed_file.close()


def test_files_time_dif_correct(directory, first_file, second_file):
    first = NetCDF(f'{directory}/{first_file}')
    second = NetCDF(f'{directory}/{second_file}')

    time_var = 'time_counter'

    print(second[time_var][:][0] - first[time_var][:][0])


# storage_path = '/home/hpc-rosneft/nfs/110_31/NEMO-ARCT/coarse_grid/'
year = 2014

storage_path = '../fixed_files'

prev_file = 'ARCTIC_1h_T_grid_T_20140929-20140929.nc'
file_to_fix = 'ARCTIC_1h_T_grid_T_20140930-20140930.nc'

# fix_missed_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix,
#                      previous_file=prev_file)

# fix_time_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix, previous_file=prev_file)

test_files_time_dif_correct(directory=f'{storage_path}/{year}',
                            first_file='ARCTIC_1h_T_grid_T_20140929-20140929.nc',
                            second_file='fixed_ARCTIC_1h_T_grid_T_20140930-20140930.nc')
