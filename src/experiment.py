import datetime
import itertools
import logging
import os
import re

from src.day import ExperimentDay
from src.day import date_range
from src.name_format import NameFormat
from src.netcdf import NCFile
from src.valid import ValidResults


class Experiment:
    def __init__(self, date_from, date_to, resulted_files):
        self._date_from = date_from
        self._date_to = date_to
        self._results_by_days = self.init_results(resulted_files)
        self._results_by_days.sort(key=lambda day: day.date)

    def init_results(self, files):
        '''
        Combine all file names into list of ExperimentDay objects
        '''
        results_by_days = self.init_blank_results()
        all_files = self.skip_some_trash_files(list(itertools.chain(*files)))
        nf = NameFormat()
        for path in all_files:
            file_name = self.path_leaf(path)
            type, error = nf.match_type(file_name)
            if error is "":
                date_str, _ = nf.match(file_name, type)
                date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
                day = next(sim_day for sim_day in results_by_days if sim_day.date == date)
                file = getattr(day, type)
                file.name = file_name
                file.path = path
            else:
                logging.info(error)

        return results_by_days

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

        valid_results = ValidResults().generate(self._date_from, self._date_to)

        errors = []
        for valid, given in zip(valid_results, self._results_by_days):
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
        for day in self._results_by_days:
            print("Integrity check for: %s" % day)
            errors_for_day = [day.ice.check_for_integrity(),
                              day.tracers.check_for_integrity(),
                              day.currents.check_for_integrity()]
            total = self._errors_in_total(errors_for_day)
            errors.append(total)
            for error in total:
                logging.error(error)

        return errors

    def check_oceanic_variables(self):
        errors = []
        for day in self._results_by_days:
            print("Variables check for: %s" % day)
            errors_for_day = [day.ice.check_variables(),
                              day.tracers.check_variables(),
                              day.currents.check_variables()]
            total = self._errors_in_total(errors_for_day)
            errors.append(total)
            for error in total:
                logging.error(error)

        return errors

    def _errors_in_total(self, errors_for_day):
        return list(filter(lambda error: error if error is not "" else None, errors_for_day))
