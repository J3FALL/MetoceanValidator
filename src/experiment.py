import datetime
import itertools
import logging
import os
import re
from multiprocessing import Pool

from tqdm import tqdm

from src.day import ExperimentDay
from src.day import date_range
from src.netcdf import NCFile
from src.valid import ValidResults

MISSING_FILE = 'missing_file'


class Experiment:
    def __init__(self, date_from, date_to, resulted_files, file_format):
        self._date_from = date_from
        self._date_to = date_to
        self.file_format = file_format

        self.matching_log = []
        self._results_by_days = self.init_results(resulted_files)
        self._results_by_days.sort(key=lambda day: day.date)

    def init_results(self, files):
        '''
        Combine all file names into list of ExperimentDay objects
        '''
        results_by_days = self.init_blank_results()
        all_files = self.skip_some_trash_files(list(itertools.chain(*files)))

        for path in all_files:
            file_name = self.path_leaf(path)
            type, error = self.file_format.match_type(file_name)
            # TODO: improve this somehow
            if error is "":
                date_str, err = self.file_format.match(file_name, type)
                if err is "":
                    date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
                    if self.date_between(date):
                        day = next(sim_day for sim_day in results_by_days if sim_day.date == date)
                        file = getattr(day, type)
                        file.name = file_name
                        file.path = path
                else:
                    self.matching_log.append(err)
            else:
                self.matching_log.append(error)

        return results_by_days

    def date_between(self, date):
        return self._date_from <= date <= self._date_to

    def init_blank_results(self):
        blank_results = []
        for date in date_range(self._date_from, self._date_to):
            blank_results.append(ExperimentDay(date=date, ice_file=NCFile(name="", path="", type="ice"),
                                               tracers_file=NCFile(name="", path="", type="tracers"),
                                               currents_file=NCFile(name="", path="", type="currents")))
        return blank_results

    def skip_some_trash_files(self, files):
        files_to_skip = re.compile(
            '|'.join(["b_gen.py", "bcondgen6.py", "create_large_net.bat", "grid.nc", "init_gen.py",
                      "initial_fill_generated_y2013.nc", "year-log.txt"]))

        return list(filter(lambda file: file if files_to_skip.match(file) is None else None, files))

    def path_leaf(self, path):
        head, tail = os.path.split(path)
        return tail

    def check_for_absence(self):
        '''
        Check whether results contain all days and each day contains
        three corresponding resulted files: [ice, tracers, currents]
        :return: List of errors
        '''

        valid_results = ValidResults(self.file_format).generate(self._date_from, self._date_to)

        errors = []
        for valid, given in tqdm(zip(valid_results, self._results_by_days), total=len(valid_results)):
            if given.is_none():
                error = "Simulation results were not found for day: %s" % valid.date.strftime("%Y%m%d")
                logging.info(error)
                errors.append(error)
            elif valid != given:
                error = "Simulation results for day: %s have some missing files or its names are incorrect: %s" % \
                        (valid.date.strftime("%Y%m%d"), given)
                logging.info(error)
                errors.append(error)

        return errors

    def check_for_integrity(self):
        errors = []
        for day in tqdm(self._results_by_days):
            print("Integrity check for: %s" % day)
            errors_for_day = [day.ice.check_for_integrity(),
                              day.tracers.check_for_integrity(),
                              day.currents.check_for_integrity()]
            total = _errors_in_total(errors_for_day)
            errors.append(total)
            for error in total:
                logging.error(error)

        return errors

    def check_oceanic_variables(self):
        errors = []
        cpu_count = 16
        with Pool(processes=cpu_count) as p:
            days_amount = len(self._results_by_days)

            with tqdm(total=days_amount) as progress_bar:
                for idx, err in tqdm(enumerate(p.imap_unordered(self.check_day, self._results_by_days))):
                    errors.extend(err)
                    progress_bar.update()

        return errors

    def check_day(self, day):
        total = []
        if not day.is_none():
            errors_for_day = []

            for var in [day.ice, day.tracers, day.currents]:

                if var.name == '':
                    continue
                integrity_error = var.check_for_integrity()

                if integrity_error is "":
                    var_errors = var.check_variables(self.file_format)
                    errors_for_day = errors_for_day + var_errors
                else:
                    errors_for_day.append(integrity_error)

            total = _errors_in_total(errors_for_day)
            for error in total:
                logging.error(error)

        return total


class WRFExperiment:
    def __init__(self, year_from, year_to, resulted_files, file_format):
        self._year_from = year_from
        self._year_to = year_to
        self.file_format = file_format

        self.results = sorted(resulted_files)

        self.matching_log = []
        self.results_by_years = self._match_results()

    def _match_results(self):

        results_by_years = self._blank_results()

        for file in self.results:
            file_name = self.path_leaf(file)
            type, error = self.file_format.match_type(file_name)
            if error is not '':
                self.matching_log.append(error)
            else:
                matched_year, _ = self.file_format.match(file_name, type)
                matched_year = int(matched_year)
                if not self.year_between(matched_year):
                    print(f"{file_name} is outside the ({self._year_from}, {self._year_to}) experiment period")
                else:
                    self._fill_year(results_by_years, file, file_name, matched_year)

        return results_by_years

    def _blank_results(self):
        return [(MISSING_FILE, year) for year in range(self._year_from, self._year_to + 1)]

    def _fill_year(self, results, path, file_name, matched_year):
        for idx in range(len(results)):
            _, year = results[idx]

            if matched_year == year:
                results[idx] = (NCFile(name=file_name, path=path, type='wrf'), matched_year)

    def path_leaf(self, path):
        head, tail = os.path.split(path)
        return tail

    def year_between(self, year):
        return self._year_from <= year <= self._year_to

    def check_for_absence(self):
        errors = []

        for results in self.results_by_years:
            file, year = results
            if file is MISSING_FILE:
                error = f"Simulation results were not found for year: {year}"
                logging.info(error)
                errors.append(error)

        return errors

    def check_variables(self):
        errors = []
        for yearly_file, year in tqdm(self.results_by_years):

            if yearly_file is not MISSING_FILE:
                error = self.check_year(yearly_file)
                errors.extend(error)

        return errors

    def check_year(self, file):
        errors_for_year = []
        integrity_error = file.check_for_integrity()
        if integrity_error is "":
            var_errors = file.check_variables(self.file_format)
            errors_for_year.extend(var_errors)
        else:
            errors_for_year.append(integrity_error)

        total = _errors_in_total(errors_for_year)
        for error in total:
            logging.error(error)

        return total


class WaveWatchExperiment:
    def __init__(self, year_from, year_to, resulted_files, file_format):
        self._year_from = year_from
        self._year_to = year_to
        self.file_format = file_format

        self.results = sorted(resulted_files)

        self.matching_log = []
        self.results_by_years = self._match_results()

    def _match_results(self):
        results_by_years = self._blank_results()

        for file in self.results:
            file_name = self.path_leaf(file)
            type, error = self.file_format.match_type(file_name)
            if error is not '':
                self.matching_log.append(error)
            else:
                date, _ = self.file_format.match(file_name, type)
                year, month = date
                if not self.year_between(year):
                    print(f"{file_name} is outside the ({self._year_from}, {self._year_to}) experiment period")
                else:
                    self._fill_month(results_by_years, file, file_name, date)

        return results_by_years

    def _blank_results(self):
        results = []

        for year in range(self._year_from, self._year_to + 1):
            for month in range(1, 13):
                results.append((MISSING_FILE, year, month))

        return results

    def path_leaf(self, path):
        head, tail = os.path.split(path)
        return tail

    def year_between(self, year):
        return self._year_from <= year <= self._year_to

    def _fill_month(self, results, path, file_name, matched_day):
        for idx in range(len(results)):
            _, year, month = results[idx]

            if matched_day == (year, month):
                results[idx] = (NCFile(name=file_name, path=path, type='waves'), year, month)

    def check_for_absence(self):
        errors = []

        for results in self.results_by_years:
            file, year, month = results
            if file is MISSING_FILE:
                error = f"Simulation results were not found for : year = {year}, month = {month}"
                logging.info(error)
                errors.append(error)

        return errors

    def check_variables(self):
        errors = []
        for monthly_file, year, month in tqdm(self.results_by_years):

            if monthly_file is not MISSING_FILE:
                error = self.check_month(monthly_file)
                errors.extend(error)

        return errors

    def check_month(self, file):

        errors_for_month = []
        integrity_error = file.check_for_integrity()
        if integrity_error is "":
            var_errors = file.check_variables(self.file_format)
            errors_for_month.extend(var_errors)
        else:
            errors_for_month.append(integrity_error)

        total = _errors_in_total(errors_for_month)
        for error in total:
            logging.error(error)

        return total


def _errors_in_total(errors_for_day):
    return list(filter(lambda error: error if error is not "" else None, errors_for_day))
