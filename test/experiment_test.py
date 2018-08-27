import unittest
from datetime import date

from src.experiment import Experiment


class ExperimentTest(unittest.TestCase):
    def test_check_for_absence(self):
        experiment = Experiment(date_from=date(2013, 1, 1), date_to=date(2013, 1, 2))

        with self.assertRaises(NotImplementedError):
            experiment.check_for_absence()
