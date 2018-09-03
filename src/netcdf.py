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

        return error

    def check_variables(self):
        errors = []

        if self.path is "":
            errors.append("%s is absent, can't be opened" % self.name)
        else:
            nc_file = NetCDF(self.path)
            nf = NameFormat()

            for correct_var in nf.variables(self.type):
                try:
                    var = nc_file.variables[correct_var]
                except KeyError:
                    error = "%s variable is not presented in %s" % (correct_var, self.name)
                    errors.append(error)

        return errors
