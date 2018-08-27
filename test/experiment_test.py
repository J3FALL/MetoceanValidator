import unittest
from datetime import date

from src.day import ExperimentDay
from src.experiment import Experiment


class ExperimentTest(unittest.TestCase):
    def test_check_for_absence_correct(self):
        results_by_days = [ExperimentDay(date=date(2013, 1, 2), ice_file='ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc',
                                         tracers_file='ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                                         currents_file='ARCTIC_1h_T_UV_20130102-20130102.nc'),
                           ExperimentDay(date=date(2013, 1, 3), ice_file='ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc',
                                         tracers_file='ARCTIC_1h_T_grid_T_20130103-20130103.nc',
                                         currents_file='ARCTIC_1h_T_UV_20130103-20130103.nc'),
                           ExperimentDay(date=date(2013, 1, 1), ice_file='ARCTIC_1h_ice_grid_TUV_20130101-20130101.nc',
                                         tracers_file='ARCTIC_1h_T_grid_T_20130101-20130101.nc',
                                         currents_file='ARCTIC_1h_T_UV_20130101-20130101.nc')
                           ]
        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 3), results_by_days=results_by_days)

        self.assertFalse(experiment.check_for_absence())

    def test_check_for_absence_missing_day(self):
        results_by_days = [ExperimentDay(date=date(2013, 1, 2), ice_file='ARCTIC_1h_ice_grid_TUV_20130102-20130102.nc',
                                         tracers_file='ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                                         currents_file='ARCTIC_1h_T_UV_20130102-20130102.nc'),
                           ExperimentDay(date=date(2013, 1, 3), ice_file='ARCTIC_1h_ice_grid_TUV_20130103-20130103.nc',
                                         tracers_file='ARCTIC_1h_T_grid_T_20130103-20130103.nc',
                                         currents_file='ARCTIC_1h_T_UV_20130103-20130103.nc')
                           ]
        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 3), results_by_days=results_by_days)
        with self.assertRaises(Exception):
            experiment.check_for_absence()

    def test_check_for_absence_missing_file(self):
        results_by_days = [ExperimentDay(date=date(2013, 1, 2), ice_file=None,
                                         tracers_file='ARCTIC_1h_T_grid_T_20130102-20130102.nc',
                                         currents_file='ARCTIC_1h_T_UV_20130102-20130102.nc')
                           ]
        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 1), results_by_days=results_by_days)
        with self.assertRaises(Exception):
            experiment.check_for_absence()
