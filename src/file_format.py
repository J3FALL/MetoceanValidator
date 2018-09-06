import logging
import os
import re

import yaml


class FileFormat:
    def __init__(self):
        self._formats = self.load_formats()
        self._vars_formats = self.init_vars_formats()

    def load_formats(self):
        with open(os.path.join(os.path.dirname(__file__), "../formats.yaml"), 'r') as stream:
            try:
                loaded = yaml.load(stream)
                return loaded
            except yaml.YAMLError as exc:
                print(exc)
                logging.info(exc)

    def init_vars_formats(self):
        vars_by_type = {}
        types = ['ice', 'tracers', 'currents']
        for type in types:
            vars_by_type[type] = []
            for var in self._formats['files'][type]['vars']:
                vars_by_type[type].append(Variable(var['name'], var['shape']))

        return vars_by_type

    def match_type(self, name):
        for type in self._formats['files'].keys():
            _, error = self.match(name, type)
            if error is "":
                return type, ""

        error = "%s has no matching type" % name
        logging.info(error)
        return "", error

    def match(self, name, type):
        '''

        :param name: name of NetCDF-file
        :param type: type of simulation result: ice, tracers or currents
        :return: extracted date as string if name matches for pattern
        '''

        pattern = self._formats['files'][type]['name']
        date = ""
        error = ""
        try:
            matches = re.search(pattern, name).groups()
            assert matches[0] == matches[1]
            date = matches[0]

        except Exception:
            error = "%s doesn't correspond to name format of %s" % (name, type)

        return date, error

    def format(self, date, type):
        return str.join("", [self._formats['files'][type]['prefix'], date.strftime(self._formats['date']),
                             "-", date.strftime(self._formats['date']), self._formats['files'][type]['suffix']])

    def variables(self, type):
        '''

        :param type: ice, tracers, currents
        :return: List of oceanic variables that must be presented in simulation result-file of a given type
        '''

        return self._vars_formats[type]


class Variable:
    def __init__(self, name, shape):
        self.name = name
        self.shape = shape

    def match(self, var):
        var_shape = list(var.shape)
        if len(self.shape) != len(var_shape) or self.shape != var_shape:
            return "Variable: %s doesn't correspond to pattern, expected: %s, actual: %s" % \
                   (self.name, str(self.shape), str(var_shape))

        return ""
