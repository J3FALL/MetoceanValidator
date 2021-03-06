import datetime
import os
import re
from shutil import copyfile
from string import Template

from netCDF4 import Dataset as NetCDF
from tqdm import tqdm

from src.ice_convert import ice_with_8_categories

file_name_patterns = [
    'ARCTIC_1h_ice_grid_TUV_(\\d{8})-(\\d{8}).nc',
    'ARCTIC_1h_T_grid_T_(\\d{8})-(\\d{8}).nc',
    'ARCTIC_1h_UV_grid_UV_(\\d{8})-(\\d{8}).nc'
]

file_name_templates = [
    Template('ARCTIC_1h_ice_grid_TUV_$date-$date.nc'),
    Template('ARCTIC_1h_T_grid_T_$date-$date.nc'),
    Template('ARCTIC_1h_UV_grid_UV_$date-$date.nc')
]

from src.logs_parser import (
    missed_files,
    missed_days,
    ice_cat_errors_files
)


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
    copyfile(f'{directory}/{previous_file}', f'{directory}/{file_to_fix}')
    fixed_file = NetCDF(f'{directory}/{file_to_fix}', mode='r+')

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


storage_path = '/home/hpc-rosneft/nfs/110_31/NEMO-ARCT/coarse_grid/'
year = 2012


# storage_path = '../fixed_files'


def fixes_example():
    prev_file = 'ARCTIC_1h_T_grid_T_19900709-19900709.nc'
    file_to_fix = 'ARCTIC_1h_T_grid_T_19900710-19900710.nc'

    fix_missed_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix,
                         previous_file=prev_file)

    fix_time_variables(directory=f'{storage_path}/{year}', file_to_fix=file_to_fix, previous_file=prev_file)

    test_files_time_dif_correct(directory=f'{storage_path}/{year}',
                                first_file='ARCTIC_1h_T_grid_T_20140929-20140929.nc',
                                second_file='fixed_ARCTIC_1h_T_grid_T_20140930-20140930.nc')

    fix_corrupted_file(directory=f'{storage_path}/{year}',
                       file_to_fix=file_to_fix, previous_file=prev_file)


def fix_missed_files_in_nfs(storage_path, log_path='../coarse_1975-1980.log'):
    missed = missed_files(log_path)

    for row in missed:
        date_raw, ice, tracers, currents = row
        date = datetime.datetime.strptime(date_raw, '%Y%m%d')
        prev_day = date - datetime.timedelta(days=1)
        prev_day_raw = prev_day.strftime('%Y%m%d')

        for file, template in zip([ice, tracers, currents], file_name_templates):
            if file is '':
                file_to_fix = template.substitute(date=date_raw)
                prev_file = template.substitute(date=prev_day_raw)

                fix_corrupted_file(directory=f'{storage_path}/{date.year}',
                                   file_to_fix=file_to_fix, previous_file=prev_file)
                print(f'FIXED: {file_to_fix}')


def fix_missed_days_in_nfs(storage_path, log_path='../coarse_1975-1980.log'):
    missed = missed_days(log_path)

    for day in missed:
        date = datetime.datetime.strptime(day, '%Y%m%d')
        prev_day = date - datetime.timedelta(days=1)
        prev_day_raw = prev_day.strftime('%Y%m%d')

        prev_files = []
        for pattern in file_name_templates:
            prev_files.append(pattern.substitute(date=prev_day_raw))

        ice, tracers, currents = prev_files

        fix_missed_day(directory=f'{storage_path}/{date.year}',
                       ice=ice, tracers=tracers, currents=currents)
        print(f'Fixed missed day: {day}')


correct_ice_file = 'ARCTIC_1h_ice_grid_TUV_19760101-19760101.nc'


def fix_ice_categories(storage_path, log_path='../coarse_1975-1980.log', cpu_count=4):
    ice_files = ice_cat_errors_files(log_path)

    for file in tqdm(ice_files):
        print(f'File to fix: {file}')
        date_raw = extracted_date_by_pattern(file)
        date = datetime.datetime.strptime(date_raw, '%Y%m%d')

        file_path = f'{storage_path}/{date.year}/{file}'

        tmp_path = f'../tmp_fixed/{date.year}'

        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)

        copyfile(f'{storage_path}/1976/{correct_ice_file}', f'{tmp_path}/{file}')

        fixed_file = NetCDF(f'{tmp_path}/{file}', mode='r+')
        file_with_errors = NetCDF(file_path, mode='r')

        for var_name in file_with_errors.variables:
            if var_name not in ['siconcat', 'sithicat', 'ncatice']:
                fixed_file[var_name][:] = file_with_errors[var_name][:]
                print(f'Variable: {var_name} was copied')
        file_with_errors.close()

        conc_fixed, thic_fixed = ice_with_8_categories(file_path=file_path, cpu_count=cpu_count)

        fixed_file['siconcat'][:] = conc_fixed
        fixed_file['sithicat'][:] = thic_fixed
        fixed_file.close()


if __name__ == '__main__':
    # fix_missed_files_in_nfs(storage_path, '../coarse_1974-2015.log')
    # fix_missed_days_in_nfs(storage_path, '../coarse_1974-2015.log')
    fix_ice_categories(storage_path, '../coarse_1974-2015.log', cpu_count=8)
