import unittest
from datetime import date

from src.experiment import Experiment
from src.experiment import WRFExperiment
from src.file_format import FileFormat


class ExperimentTest(unittest.TestCase):
    def test_check_for_absence_correct(self):
        results = [['ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc', 'ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                    'ARCTIC_1h_UV_grid_UV_20130102-20130102.nc'],
                   ['ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc', 'ARCTIC_1h_T_grid_T_20130103-20130103.nc',
                    'ARCTIC_1h_UV_grid_UV_20130103-20130103.nc'],
                   ['ARCTIC_1h_ice_grid_TUV_20130101-20130101.nc', 'ARCTIC_1h_T_grid_T_20130101-20130101.nc',
                    'ARCTIC_1h_UV_grid_UV_20130101-20130101.nc']]

        format = FileFormat(format_file="../formats/formats.yaml")
        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 3),
                                resulted_files=results, file_format=format)

        self.assertEqual(len(experiment.check_for_absence()), 0)

    def test_check_for_absence_missing_day(self):
        results = [['ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc', 'ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                    'ARCTIC_1h_UV_grid_UV_20130102-20130102.nc'],
                   ['ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc', 'ARCTIC_1h_T_grid_T_20130103-20130103.nc',
                    'ARCTIC_1h_UV_grid_UV_20130103-20130103.nc']]
        format = FileFormat(format_file="../formats/formats.yaml")
        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 3),
                                resulted_files=results, file_format=format)

        errors = experiment.check_for_absence()

        error = "Simulation results were not found for day: 20130101"
        self.assertEqual(len(errors), 1)
        self.assertIn(error, errors[0])

    def test_check_for_absence_missing_file(self):
        results = [['ARCTIC_1h_T_grid_T_20130101-20130101.nc', 'ARCTIC_1h_UV_grid_UV_20130101-20130101.nc']]
        format = FileFormat(format_file="../formats/formats.yaml")

        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 1),
                                resulted_files=results, file_format=format)

        errors = experiment.check_for_absence()

        error = "Simulation results for day: 20130101 have some missing files or its names are incorrect"
        self.assertEqual(len(errors), 1)
        self.assertIn(error, errors[0])


class WRFExperimentTest(unittest.TestCase):
    def test_check_for_absence_correct(self):
        exp = WRFExperiment(year_from=2000, year_to=2000,
                            resulted_files=['../wrf.2000.nc'], file_format=FileFormat('../formats/wrf-formats.yaml'))
        errors = exp.check_for_absence()

        self.assertEqual(len(errors), 0)

    def test_check_for_absence_missing_files(self):
        exp = WRFExperiment(year_from=2000, year_to=2005,
                            resulted_files=['../wrf.2000.nc'], file_format=FileFormat('../formats/wrf-formats.yaml'))

        errors = exp.check_for_absence()

        expected_missed_years = 5
        expected_error = 'Simulation results were not found for year: 2001'

        self.assertEqual(len(errors), expected_missed_years)
        self.assertIn(expected_error, errors)
