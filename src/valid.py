from src.day import ExperimentDay
from src.day import date_range
from src.name_format import NameFormat


class ValidResults:
    def __init__(self):
        self.name_format = NameFormat()

    def generate(self, from_date, to_date):
        '''
        Generates a list with all valid simulation results names for a given period.
        Time delta = 1 day.
        :return: for each day three names are returned: [ice, tracers, currents]
        '''

        results = []
        for date in date_range(from_date, to_date):
            results.append(ExperimentDay(date=date, ice_file=self.name_format.format(date, 'ice'),
                                         tracers_file=self.name_format.format(date, 'tracers'),
                                         currents_file=self.name_format.format(date, 'currents')))

        return results
