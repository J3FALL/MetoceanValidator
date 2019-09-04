import unittest
from datetime import date

from src.file_format import FileFormat


class FileFormatTest(unittest.TestCase):

    def test_matching_correct(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')

        ice_file = "ARCTIC_1h_ice_grid_TUV_20130105-20130105.nc"
        currents_file = "ARCTIC_1h_UV_grid_UV_20140306-20140306.nc"
        tracers_file = "ARCTIC_1h_T_grid_T_20010203-20010203.nc"

        self.assertEqual(nf.match(ice_file, "ice"), ("20130105", ""))
        self.assertEqual(nf.match(currents_file, "currents"), ("20140306", ""))
        self.assertEqual(nf.match(tracers_file, "tracers"), ("20010203", ""))

    def test_matching_wrong_type(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')
        ice_file = "ARCTIC_1h_ice_grid_TUV_20130105-20130105.nc"
        date, error = nf.match(ice_file, "tracers")
        self.assertEqual(date, "")
        self.assertEqual(error, "%s doesn't correspond to name format of tracers" % ice_file)

    def test_matching_incorrect(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')

        diff_dates = "ARCTIC_1h_ice_grid_TUV_20130105-20130106.nc"
        incorrect_name = "ARCTIC_1h_ice_XXX_TUV_20130105-20130105.n"

        date, error = nf.match(diff_dates, "ice")
        self.assertEqual(date, "")
        self.assertEqual(error, "%s doesn't correspond to name format of ice" % diff_dates)

        date, error = nf.match(incorrect_name, "ice")
        self.assertEqual(date, "")
        self.assertEqual(error, "%s doesn't correspond to name format of ice" % incorrect_name)

    def test_format_correct(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')

        source_date = date(2013, 1, 15)
        formatted_date = "ARCTIC_1h_ice_grid_TUV_20130115-20130115.nc"

        self.assertEqual(nf.format(source_date, "ice"), formatted_date)

    def test_match_type_correct(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')

        file = "ARCTIC_1h_ice_grid_TUV_20130115-20130115.nc"

        actual_type, error = nf.match_type(file)
        self.assertEqual(error, "")
        self.assertEqual(actual_type, "ice")

    def test_match_type_incorrect(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')

        file = "ARCTIC_1h_floor_grid_TUV_20130115-20130115.nc"

        actual_type, error = nf.match_type(file)

        expected_error = "%s has no matching type" % file
        self.assertEqual(error, expected_error)
        self.assertEqual(actual_type, "")

    def test_variables(self):
        nf = FileFormat('../formats/nemo14-formats.yaml')

        expected_var_names = ['deptht', 'deptht_bounds', 'nav_lat', 'nav_lon', 'sossheig', 'vosaline', 'votemper']
        actual_var_names = [var.name for var in nf.variables('tracers')]
        self.assertListEqual(expected_var_names, actual_var_names)
