import datetime
import itertools

from src.day import ExperimentDay
from src.day import date_range
from src.name_format import NameFormat
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
        all_files = list(itertools.chain(*files))

        nf = NameFormat()
        for file in all_files:
            type = nf.match_type(file)
            date = datetime.datetime.strptime(nf.match(file, type), "%Y%m%d").date()
            day = next(sim_day for sim_day in results_by_days if sim_day.date == date)
            setattr(day, type, file)

        return results_by_days

    def init_blank_results(self):
        blank_results = []
        for date in date_range(self._date_from, self._date_to):
            blank_results.append(ExperimentDay(date))
        return blank_results

    def check_for_absence(self):
        '''
        Check whether results contain all days and each day contains
        three corresponding resulted files: [ice, tracers, currents]
        :return: False if all resulted files are presented, otherwise exceptions were raised
        '''

        valid_results = ValidResults().generate(self._date_from, self._date_to)

        for valid, given in zip(valid_results, self._results_by_days):

            if given.is_none:
                error = "Simulation results were not found for day: %s" % valid.date.strftime("%Y%m%d")
                raise Exception(error)
            elif valid != given:
                error = "Simulation results for day: %s have some missing files or its names are incorrect: %s" % \
                        (valid.date.strftime("%Y%m%d"), given)
                raise Exception(error)

        return False
