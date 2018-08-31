import unittest

from src.netcdf import NCFile


class NCFileTest(unittest.TestCase):

    def test_check_for_integrity_correct(self):
        file = NCFile("correct.nc", "netcdf/correct.nc", "any")
        error = file.check_for_integrity()

        self.assertEqual(error, "")

    def test_check_for_integrity_corrupted_file(self):
        file = NCFile("corrupted.nc", "netcdf/corrupted.nc", "any")
        error = file.check_for_integrity()

        self.assertEqual(error, "corrupted.nc can't be opened")
