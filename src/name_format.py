import re

import yaml


class NameFormat:
    def __init__(self):
        self._formats = self.load_formats()

    def load_formats(self):
        with open("../formats.yaml", 'r') as stream:
            try:
                loaded = yaml.load(stream)
                return loaded
            except yaml.YAMLError as exc:
                print(exc)

    def match_type(self, name):
        for type in self._formats.keys():
            try:
                self.match(name, type)
                return type
            except Exception:
                continue

        error = "%s has no matching type" % name
        raise Exception(error)

    def match(self, name, type):
        '''

        :param name: name of NetCDF-file
        :param type: type of simulation result: ice, tracers or currents
        :return: extracted date as string if name matches for pattern
        '''

        pattern = self._formats[type]['name']

        try:
            matches = re.search(pattern, name).groups()
            assert matches[0] == matches[1]
            return matches[0]
        except Exception as exc:
            error = "%s doesn't correspond to name format of %s" % (name, type)
            raise RuntimeError(error, exc)

    def format(self, date, type):
        return str.join("", [self._formats[type]['prefix'], date.strftime(self._formats['date']),
                             "-", date.strftime(self._formats['date']), self._formats[type]['suffix']])
