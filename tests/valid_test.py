import unittest
from datetime import date

from src.day import ExperimentDay
from src.netcdf import NCFile
from src.valid import ValidResults


class ValidResultsTest(unittest.TestCase):

    def test_valid_results(self):
        results = ValidResults()

        date_from = date(2013, 1, 1)
        date_to = date(2013, 1, 3)

        expected_results = [ExperimentDay(date=date(2013, 1, 1),
                                          ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20130101-20130101.nc', path='',
                                                          type='ice'),
                                          tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20130101-20130101.nc', path='',
                                                              type='tracers'),
                                          currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20130101-20130101.nc',
                                                               path='', type='currents')),
                            ExperimentDay(date=date(2013, 1, 2),
                                          ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc', path='',
                                                          type='ice'),
                                          tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20130102-20130102.nc', path='',
                                                              type='tracers'),
                                          currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20130102-20130102.nc',
                                                               path='', type='currents')),
                            ExperimentDay(date=date(2013, 1, 3),
                                          ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc', path='',
                                                          type='ice'),
                                          tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20130103-20130103.nc', path='',
                                                              type='tracers'),
                                          currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20130103-20130103.nc',
                                                               path='', type='currents'))
                            ]
        all_results = results.generate(date_from, date_to)

        for expected, real in zip(expected_results, all_results):
            self.assertEqual(expected, real)
