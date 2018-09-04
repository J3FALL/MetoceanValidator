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

            for correct_var in nf.variables(self.type):
                try:
                    var = nc_file.variables[correct_var.name]
                    error = self.check_shape(var, correct_var)
                    if error is not "":
                        errors.append(error)
                except KeyError:
                    error = "%s variable is not presented in %s" % (correct_var, self.name)
                    errors.append(error)

        return errors

    def check_shape(self, var, correct_var):
        return correct_var.match(var)
