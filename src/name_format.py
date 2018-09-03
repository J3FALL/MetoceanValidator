import logging
import os
import re

import yaml


class NameFormat:
    def __init__(self):
        self._formats = self.load_formats()

    def load_formats(self):
        with open(os.path.join(os.path.dirname(__file__), "../formats.yaml"), 'r') as stream:
            try:
                loaded = yaml.load(stream)
                return loaded
            except yaml.YAMLError as exc:
                print(exc)
                logging.info(exc)

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

        return self._formats['files'][type]['vars']
