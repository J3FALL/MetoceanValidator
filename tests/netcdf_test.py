import os
import unittest

from src.netcdf import NCFile


class NCFileTest(unittest.TestCase):

    def test_check_for_integrity_correct(self):
        file = NCFile("correct.nc", os.path.join(os.path.dirname(__file__), "netcdf/correct.nc"), "any")
        error = file.check_for_integrity()

        self.assertEqual(error, "")

    def test_check_for_integrity_corrupted_file(self):
        file = NCFile("corrupted.nc", os.path.join(os.path.dirname(__file__), "netcdf/corrupted.nc"), "any")
        error = file.check_for_integrity()

        self.assertEqual(error, "corrupted.nc can't be opened")
