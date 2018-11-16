from src.day import ExperimentDay
from src.day import date_range
from src.file_format import FileFormat
from src.netcdf import NCFile


class ValidResults:
    def __init__(self, file_format):
        self.file_format = file_format

    def generate(self, from_date, to_date):
        '''
        Generates a list with all valid simulation results names for a given period.
        Time delta = 1 day.
        :return: for each day three names are returned: [ice, tracers, currents]
        '''

        results = []
        for date in date_range(from_date, to_date):
            results.append(ExperimentDay(date=date,
                                         ice_file=NCFile(name=self.file_format.format(date, 'ice'), path='',
                                                         type='ice'),
                                         tracers_file=NCFile(name=self.file_format.format(date, 'tracers'), path='',
                                                             type='tracers'),
                                         currents_file=NCFile(name=self.file_format.format(date, 'currents'), path='',
                                                              type='currents')))
        return results
