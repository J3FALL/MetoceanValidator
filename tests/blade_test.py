import unittest
from datetime import date
from unittest.mock import patch

from src.blade import BladeChecker
from src.file_format import FileFormat


class BladeTest(unittest.TestCase):
    mocked_nc_files = ['ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc',
                       'ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                       'ARCTIC_1h_UV_grid_UV_20130102-20130102.nc',
                       'ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc',
                       'ARCTIC_1h_T_grid_T_20130103-20130103.nc',
                       'ARCTIC_1h_UV_grid_UV_20130103-20130103.nc',
                       'ARCTIC_1h_ice_grid_TUV_20130101-20130101.nc',
                       'ARCTIC_1h_T_grid_T_20130101-20130101.nc',
                       'ARCTIC_1h_UV_grid_UV_20130101-20130101.nc']

    def setUp(self):
        self.checker = BladeChecker(date_from=date(2013, 1, 1), date_to=date(2013, 1, 3),
                                    file_format=FileFormat('../formats/formats.yaml'))

    @patch('src.blade.BladeChecker.get_all_netcdf_files', return_value=mocked_nc_files)
    def test_check_local_storage_for_absence_correct(self, _):
        self.assertEqual(len(self.checker.check_nemo_files(mode="absence")), 0)
