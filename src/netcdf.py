import numpy as np
from netCDF4 import Dataset as NetCDF
from numpy.ma import MaskedArray


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
        except OSError:
            error = "%s can't be opened" % self.name

        return error

    def check_variables(self, file_format):
        errors = []

        if self.path is "":
            errors.append("%s is absent, can't be opened" % self.name)
        else:
            nc_file = NetCDF(self.path)

            for correct_var in file_format.variables(self.type):
                try:
                    var = nc_file.variables[correct_var.name]
                    error = self.check_shape(var, correct_var, self.name)
                    if error is not "":
                        errors.append(error)

                    # TODO: change magic constants with more smart calculations
                    if self.check_for_nan(var, 200, 200):
                        error = f"{var.name} variable has NaN-value at (200,200) point in {self.name}"
                        errors.append(error)
                except KeyError:
                    error = "%s variable is not presented in %s" % (correct_var.name, self.name)
                    errors.append(error)

        return errors

    def check_shape(self, var, correct_var, file_name):
        if self.type is not 'wrf':
            return correct_var.match(var, file_name)
        else:
            return correct_var.match(var, file_name, wrf=True)

    def check_for_constant_values(self, var):
        # CHECK ONLY TIME[0] FOR SPEED BOOST
        unique = np.unique(var)
        return len(unique) == 1

    def check_for_nan(self, var, x, y):
        fixed_idx = 0

        if isinstance(var, MaskedArray):
            nan_value = var.fill_value
            array = filled_ndarray(var)

            slice = sliced_array(array, fixed_idx, 2)

            if slice[x, y] == nan_value:
                return True

        return False


def filled_ndarray(masked_array):
    assert isinstance(masked_array, MaskedArray)
    return masked_array.data


def sliced_array(array, fixed_idx, last_dims):
    '''
    Dumb way to get slize of array like array[fixed_idx][fixed_idx].....[][] up to last_dims
    '''

    slice = array
    shape = slice.shape

    for _ in range(len(shape) - last_dims):
        slice = slice[fixed_idx]

    return slice
