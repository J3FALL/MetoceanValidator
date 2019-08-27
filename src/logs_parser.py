import re

MISSED_FILES_PATTERN = '\w*Simulation results for day: ([0-9]{8}) have some missing files or its names are incorrect:' \
                       ' date: [0-9]{8}, ice_file: ([\w\W]*), tracers_file: ([\w\W]*), currents_file: ([\w\W]*)\n'

MISSED_DAY_PATTERN = '\w*Simulation results were not found for day: ([0-9]{8})'

CORRUPTED_FILE_PATTERN = 'ERROR:root:([\w\W]*) can\'t be opened'

ICE_CATEGORIES_PATTERN = 'ERROR:root:([\w\W]*) Variable: ncatice doesn\'t correspond to pattern'


def missed_files(log_file_path):
    pattern = re.compile(MISSED_FILES_PATTERN)

    missed = []
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            for match in re.finditer(pattern, line):
                date, ice, tracers, currents = match.groups()
                missed.append([date, ice, tracers, currents])
    return missed


def missed_days(log_file_path):
    pattern = re.compile(MISSED_DAY_PATTERN)

    missed = []
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            for match in re.finditer(pattern, line):
                date = match.groups()
                missed.append(date)
    return missed


def corrupted_files(log_file_path):
    pattern = re.compile(CORRUPTED_FILE_PATTERN)

    corrupted = []
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            for match in re.finditer(pattern, line):
                file_name = match.groups()[0]
                corrupted.append(file_name)
    return corrupted


def ice_cat_errors_files(log_file_path):
    pattern = re.compile(ICE_CATEGORIES_PATTERN)

    ice_files = []
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            for match in re.finditer(pattern, line):
                file_name = match.groups()[0]
                ice_files.append(file_name)
    return ice_files


if __name__ == '__main__':
    coarse_log = '../coarse_1970-75.log'
    missed = missed_files(coarse_log)
    print(f'missed_files: {len(missed)}')
    missed = missed_days(coarse_log)
    print(f'missed_days: {len(missed)}')
    corrupted = corrupted_files(coarse_log)
    print(f'corrupted_files: {len(corrupted)}')
    ice_files = ice_cat_errors_files(coarse_log)
    print(f'ice categories files: {len(ice_files)}')
