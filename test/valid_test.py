import unittest
from datetime import date

from src.valid import ValidResults


class ValidResultsTest(unittest.TestCase):

    def test_valid_results(self):
        results = ValidResults()

        date_from = date(2013, 1, 1)
        date_to = date(2013, 1, 3)
        expected_names = [['ARCTIC_1h_ice_grid_TUV_20130101-20130101.nc', 'ARCTIC_1h_T_grid_T_20130101-20130101.nc',
                           'ARCTIC_1h_T_UV_20130101-20130101.nc'],
                          ['ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc', 'ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                           'ARCTIC_1h_T_UV_20130102-20130102.nc'],
                          ['ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc', 'ARCTIC_1h_T_grid_T_20130103-20130103.nc',
                           'ARCTIC_1h_T_UV_20130103-20130103.nc']]
        all_names = results.generate(date_from, date_to)

        for expected, real in zip(expected_names, all_names):
            self.assertListEqual(expected, real)
