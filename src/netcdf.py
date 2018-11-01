import numpy as np
from netCDF4 import Dataset as NetCDF

from src.file_format import FileFormat


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

        return error

    def check_variables(self):
        errors = []

        if self.path is "":
            errors.append("%s is absent, can't be opened" % self.name)
        else:
            nc_file = NetCDF(self.path)
            nf = FileFormat()

            # print("Variables checking in %s " % self.name)
            for correct_var in nf.variables(self.type):
                try:
                    var = nc_file.variables[correct_var.name]
                    error = self.check_shape(var, correct_var)
                    if error is not "":
                        errors.append(error)
                    # print("%s: checking for constants: %s" % (datetime.datetime.now().time(), correct_var.name))
                    # if self.check_for_constant_values(var):
                    #     error = "%s variable is filled constant value only in %s" % (var.name, self.name)
                    #     errors.append(error)
                except KeyError:
                    error = "%s variable is not presented in %s" % (correct_var, self.name)
                    errors.append(error)

        return errors

    def check_shape(self, var, correct_var):
        return correct_var.match(var)

    def check_for_constant_values(self, var):
        # CHECK ONLY TIME[0] FOR SPEED BOOST
        unique = np.unique(var)
        return len(unique) == 1
