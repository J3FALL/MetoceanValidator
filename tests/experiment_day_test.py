import unittest
from datetime import date

from src.day import ExperimentDay
from src.netcdf import NCFile


class ExperimentDayTest(unittest.TestCase):
    def test_equals(self):
        first = ExperimentDay(date=date(2014, 2, 15),
                              ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20140215-20140215.nc', path='', type='ice'),
                              tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20140215-20140215.nc', path='',
                                                  type='tracers'),
                              currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20140215-20140215.nc', path='',
                                                   type='currents'))
        second = ExperimentDay(date=date(2014, 2, 15),
                               ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20140215-20140215.nc', path='', type='ice'),
                               tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20140215-20140215.nc', path='',
                                                   type='tracers'),
                               currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20140215-20140215.nc', path='',
                                                    type='currents'))
        self.assertEqual(first, second)

    def test_not_equals(self):
        first = ExperimentDay(date=date(2014, 2, 15),
                              ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20140215-20140215.nc', path='', type='ice'),
                              tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20140215-20140215.nc', path='',
                                                  type='tracers'),
                              currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20140215-20140215.nc', path='',
                                                   type='currents'))
        second = ExperimentDay(date=date(2015, 2, 15),
                               ice_file=NCFile(name='ARCTIC_1h_ice_grid_TUV_20150215-20150215.nc', path='', type='ice'),
                               tracers_file=NCFile(name='ARCTIC_1h_T_grid_T_20150215-20150215.nc', path='',
                                                   type='tracers'),
                               currents_file=NCFile(name='ARCTIC_1h_UV_grid_UV_20150215-20150215.nc', path='',
                                                    type='currents'))

        self.assertNotEqual(first, second)
