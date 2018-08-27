import unittest
from datetime import date

from src.experiment import ExperimentDay


class ExperimentDayTest(unittest.TestCase):
    def test_equals(self):
        first = ExperimentDay(date=date(2014, 2, 15), ice_file='ARCTIC_1h_ice_grid_TUV_20140215-20140215.nc',
                              tracers_file='ARCTIC_1h_T_grid_T_20140215-20140215.nc',
                              currents_file='ARCTIC_1h_T_UV_20140215-20140215.nc')
        second = ExperimentDay(date=date(2014, 2, 15), ice_file='ARCTIC_1h_ice_grid_TUV_20140215-20140215.nc',
                               tracers_file='ARCTIC_1h_T_grid_T_20140215-20140215.nc',
                               currents_file='ARCTIC_1h_T_UV_20140215-20140215.nc')

        self.assertEqual(first, second)

    def test_not_equals(self):
        first = ExperimentDay(date=date(2014, 2, 15), ice_file='ARCTIC_1h_ice_grid_TUV_20140215-20140215.nc',
                              tracers_file='ARCTIC_1h_T_grid_T_20140215-20140215.nc',
                              currents_file='ARCTIC_1h_T_UV_20140215-20140215.nc')
        second = ExperimentDay(date=date(2015, 2, 15), ice_file='ARCTIC_1h_ice_grid_TUV_20150215-20150215.nc',
                               tracers_file='ARCTIC_1h_T_grid_T_20150215-20150215.nc',
                               currents_file='ARCTIC_1h_T_UV_20150215-20150215.nc')

        self.assertNotEqual(first, second)
