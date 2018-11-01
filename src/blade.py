import glob
import logging
import os

from src.experiment import Experiment


class BladeChecker:
    def __init__(self, date_from, date_to):
        self._storage_path = os.environ['STORAGE_PATH']
        self._date_from = date_from
        self._date_to = date_to
        self.init_logging()
        self.experiment = ""

    def init_logging(self):
        logging.basicConfig(filename='../logs/errors.log', level=logging.INFO, filemode='w')

    def check_local_storage(self, mode="absence"):
        logging.info('Started')
        files = self.get_all_netcdf_files()
        print("files amount : %d" % len(files))
        self.experiment = Experiment(date_from=self._date_from, date_to=self._date_to, resulted_files=[files])

        if mode == "absence":
            errors = self.experiment.check_for_absence()
            self.summary(errors, [])

            logging.info('Finished')

            return errors
        else:

            absence_errors = self.experiment.check_for_absence()
            vars_errors = self.experiment.check_oceanic_variables()
            self.summary(absence_errors, vars_errors)

            logging.info('Finished')

            return absence_errors + vars_errors

    def get_all_netcdf_files(self):
        files = []
        for file_name in glob.iglob(self._storage_path + "**/*.nc", recursive=True):
            files.append(file_name)
        return files

    # TODO: extract class or/and Error class
    def summary(self, absence_errors, vars_errors):
        self.dump_matching_errors()
        print("absence errors total: %d, including:" % len(absence_errors))
        no_matching = list(filter(lambda error: error if "no matching type" in error else None, absence_errors))
        not_found_days = list(filter(lambda error: error if "were not found" in error else None, absence_errors))
        not_found_files = list(filter(lambda error: error if "some missing files" in error else None, absence_errors))
        print("     no matching type: %d" % len(no_matching))
        print("      missing days: %d" % len(not_found_days))
        print("      missing files/incorrect file names: %d" % len(not_found_files))

        print("variable errors total: %d, including:" % len(vars_errors))
        with_constants = list(filter(lambda error: error if "constant value" in error else None, vars_errors))
        wrong_shape = list(filter(lambda error: error if "doesn't correspond to" in error else None, vars_errors))
        missing_vars = list(filter(lambda error: error if "variable is not presented" in error else None, vars_errors))
        print("     with constant values: %d" % len(with_constants))
        print("     with wrong shape: %d" % len(wrong_shape))
        print("     with missing variable: %d" % len(missing_vars))

    def dump_matching_errors(self):
        with open('../logs/matching_errors.log', 'w') as file:
            for error in self.experiment.matching_log:
                file.write(error + "\n")
