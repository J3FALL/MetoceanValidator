import logging

from netCDF4 import Dataset as NetCDF

from src.name_format import NameFormat


class NCFile:
    def __init__(self, name, path, type):
        self.name = name
        self.path = path
        self.type = type

    def check_for_integrity(self):
        error = ""
        try:
            nc_file = NetCDF(self.path)
            nc_file.close()
        except OSError as exc:
            print(exc)
            error = "%s can't be opened" % self.name
            logging.error(error)

        return error

    def check_variables(self):
        nc_file = NetCDF(self.path)
        nf = NameFormat()

        errors = []
        for correct_var in nf.variables(self.type):
            try:
                var = nc_file.variables[correct_var]
            except KeyError:
                error = "%s variable is not presented in %s" % (correct_var, self.name)
                logging.error(error)
                errors.append(error)

        print("%s check_variables: done" % self.name)
        return errors
