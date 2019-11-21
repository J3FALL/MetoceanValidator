import glob
import logging
import os

from src.experiment import (
    Experiment,
    WRFExperiment,
    WaveWatchExperiment
)
from src.ftp import missed_years

TEMP_DIR = "../temp_missed"


class BladeChecker:
    def __init__(self, date_from, date_to, file_format, storage_path, log_file_path='../logs/errors.log'):
        self.__storage_path = storage_path
        self._date_from = date_from
        self._date_to = date_to
        self.file_format = file_format
        self.init_logging(log_file_path=log_file_path)
        self.experiment = ""

    def init_logging(self, log_file_path):
        logging.basicConfig(filename=log_file_path, level=logging.INFO, filemode='w')

    def check_nemo_files(self, mode="absence", summary=False):
        logging.info('Started')
        files = self.get_all_netcdf_files()
        print("files amount : %d" % len(files))
        self.experiment = Experiment(date_from=self._date_from, date_to=self._date_to,
                                     resulted_files=[files], file_format=self.file_format)

        if mode == "absence":
            errors = self.experiment.check_for_absence()
            if summary:
                self.summary(errors, [])

            logging.info('Finished')

            return errors
        else:

            absence_errors = self.experiment.check_for_absence()
            vars_errors = self.experiment.check_oceanic_variables()

            if summary:
                self.summary(absence_errors, vars_errors)

            logging.info('Finished')

            return absence_errors + vars_errors

    def get_all_netcdf_files(self):
        files = []
        for file_name in glob.iglob(self.__storage_path + "**/*.nc", recursive=True):
            files.append(file_name)

        return files

    def check_storage_with_ftp(self, storage, mode='absence', summary=False):
        logging.info('Started')
        files = self.combined_file_names(storage)
        print("files amount : %d" % len(files))

        self.experiment = Experiment(date_from=self._date_from, date_to=self._date_to,
                                     resulted_files=[files], file_format=self.file_format)

        if mode == 'absence':
            errors = self.experiment.check_for_absence()
            if summary:
                self.summary(errors, [])

            logging.info('Finished')

            return errors

    def combined_file_names(self, ftp_storage):
        '''
        Creates a list with all resulted files for each year.
            If files for a year are stored in mounted disk then join its names with mount_dir.
            Else connect to ftp_storage, find all files for a year and join all file names that were found
                with virtual TEMP_DIR.
        :param ftp_storage: FtpStorage class
        '''
        files = []
        missed_years_ = missed_years(ftp_storage)

        for dir in ftp_storage.dirs:
            if dir.year in missed_years_:
                files_from_ftp = [os.path.join(TEMP_DIR, dir.year, file)
                                  for file in ftp_storage.file_names_by_year(dir.year)]
                files.extend(files_from_ftp)
            else:
                files_local = [file for file in
                               glob.iglob(os.path.join(ftp_storage.mount_dir_by_year(dir.year), dir.path) + "**/*.nc",
                                          recursive=True)]
                files.extend(files_local)

        return files

    def check_wrf_files(self, mode='absence', summary=False):
        logging.info('Started')

        files = self.wrf_yearly_files()

        self.experiment = WRFExperiment(year_from=self._date_from.year, year_to=self._date_to.year,
                                        resulted_files=files, file_format=self.file_format)
        if mode == 'absence':
            errors = self.experiment.check_for_absence()
            if summary:
                self.summary(errors, [])

            logging.info('Finished')
            return errors

        else:
            absence_errors = self.experiment.check_for_absence()
            vars_errors = self.experiment.check_variables()

            if summary:
                self.summary(absence_errors, vars_errors)

            logging.info('Finished')

            return absence_errors + vars_errors

    def wrf_yearly_files(self):
        files = []
        for file_name in glob.iglob(self.__storage_path + "**/*.nc", recursive=True):
            files.append(file_name)

        return files

    def check_wave_watch_files(self, mode='absence', summary=False):

        files = self.wave_watch_monthly_files()

        self.experiment = WaveWatchExperiment(year_from=self._date_from.year, year_to=self._date_to.year,
                                              resulted_files=files, file_format=self.file_format)

        if mode == 'absence':
            errors = self.experiment.check_for_absence()
            if summary:
                self.summary(errors, [])

            logging.info('Finished')
            return errors
        else:
            absence_errors = self.experiment.check_for_absence()
            vars_errors = self.experiment.check_variables()

            if summary:
                self.summary(absence_errors, vars_errors)

            logging.info('Finished')

            return absence_errors + vars_errors

    def wave_watch_monthly_files(self):
        files = []
        for file_name in glob.iglob(self.__storage_path + '**/*.nc', recursive=True):
            files.append(file_name)

        return files

    # TODO: extract class or/and Error class
    def summary(self, absence_errors, vars_errors):
        self.dump_matching_errors()

        with open('../logs/errors_summary.log', 'w') as file:
            file.write("absence errors total: %d, including:\n" % len(absence_errors))

            no_matching = list(filter(lambda error: error if "no matching type" in error else None, absence_errors))
            not_found_days = list(filter(lambda error: error if "were not found" in error else None, absence_errors))
            not_found_files = list(
                filter(lambda error: error if "some missing files" in error else None, absence_errors))

            file.write('\tno matching type: %d\n' % len(no_matching))
            file.write('\tmissing days: %d\n' % len(not_found_days))
            file.write('\tmissing files/incorrect file names: %d\n' % len(not_found_files))

            file.write('variable errors total: %d, including:\n' % len(vars_errors))

            with_constants = list(filter(lambda error: error if "constant value" in error else None, vars_errors))
            wrong_shape = list(filter(lambda error: error if "doesn't correspond to" in error else None, vars_errors))
            missing_vars = list(
                filter(lambda error: error if "variable is not presented" in error else None, vars_errors))
            nan_values = list(filter(lambda error: error if "has NaN-value" in error else None, vars_errors))

            file.write('\twith constant values: %d\n' % len(with_constants))
            file.write('\twith wrong shape: %d\n' % len(wrong_shape))
            file.write('\twith missing variable: %d\n' % len(missing_vars))
            file.write('\twith NaNs: %d\n' % len(nan_values))

    def dump_matching_errors(self):
        with open('../logs/matching_errors.log', 'w') as file:
            for error in self.experiment.matching_log:
                file.write(error + "\n")


def _l2_local_files(storage_path, year_from=1964, year_to=2016):
    files = []
    dirs = [str(year) for year in range(year_from, year_to)]

    for dir in dirs:
        for file_name in glob.iglob(
                storage_path + f"L2-{dir}/*/*.nc", recursive=True):
            files.append(file_name)
        for file_name in glob.iglob(
                storage_path + f"L2-{dir}/*.nc", recursive=True):
            files.append(file_name)

    return files
