import unittest

from src.matching import NameFormat


class NameMatchingTest(unittest.TestCase):

    def test_matching_correct(self):
        nf = NameFormat()

        ice_file = "ARCTIC_1h_ice_grid_TUV_20130105-20130105.nc"
        currents_file = "ARCTIC_1h_T_UV_20140306-20140306.nc"
        tracers_file = "ARCTIC_1h_T_grid_T_20010203-20010203.nc"

        self.assertEqual(nf.match(ice_file, "ice"), "20130105")
        self.assertEqual(nf.match(currents_file, "currents"), "20140306")
        self.assertEqual(nf.match(tracers_file, "tracers"), "20010203")

    def test_matching_wrong_type(self):
        nf = NameFormat()
        ice_file = "ARCTIC_1h_ice_grid_TUV_20130105-20130105.nc"
        with self.assertRaises(RuntimeError):
            nf.match(ice_file, "tracers")

    def test_matching_incorrect(self):
        nf = NameFormat()

        diff_dates = "ARCTIC_1h_ice_grid_TUV_20130105-20130106.nc"
        incorrect_name = "ARCTIC_1h_ice_XXX_TUV_20130105-20130105.n"

        with self.assertRaises(RuntimeError):
            nf.match(diff_dates, "ice")
        with self.assertRaises(RuntimeError):
            nf.match(incorrect_name, "ice")
