import logging

from netCDF4 import Dataset as NetCDF


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
            logging.error(error)

        return error
