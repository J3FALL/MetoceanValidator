from shutil import copyfile

from netCDF4 import Dataset as NetCDF


def fix_missed_variables(directory, file_to_fix, previous_file):
    copyfile(f'{directory}/{previous_file}', f'{directory}/fixed_{file_to_fix}')
    file_with_errors = NetCDF(f'{directory}/{file_to_fix}', mode='r')
    fixed_file = NetCDF(f'{directory}/fixed_{file_to_fix}', mode='r+')

    for var_name in file_with_errors.variables:
        fixed_file[var_name][:] = file_with_errors[var_name][:]

    file_with_errors.close()
    fixed_file.close()


# storage_path = '/home/hpc-rosneft/nfs/110_31/NEMO-ARCT/coarse_grid/'
year = 2004

storage_path = '../fixed_files'

file_to_fix = 'ARCTIC_1h_T_grid_T_20040509-20040509.nc'
prev_file = 'ARCTIC_1h_T_grid_T_20040508-20040508.nc'

fix_missed_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix,
                     previous_file=prev_file)
