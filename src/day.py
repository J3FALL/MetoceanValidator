from datetime import timedelta


class ExperimentDay:
    def __init__(self, date, ice_file=None, tracers_file=None, currents_file=None):
        self.date = date
        self.ice = ice_file
        self.tracers = tracers_file
        self.currents = currents_file

    def is_none(self):
        return self.ice.name is "" and self.tracers.name is "" and self.currents.name is ""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.date == other.date and self.ice.name == other.ice.name and \
                   self.tracers.name == other.tracers.name and \
                   self.currents.name == other.currents.name
        return False

    def __ne__(self, other):
        return self.date != other.date or self.ice.name != other.ice.name or \
               self.tracers.name != other.tracers.name or \
               self.currents.name != other.currents.name

    def __str__(self):
        return "date: %s, ice_file: %s, tracers_file: %s, currents_file: %s" % \
               (self.date.strftime("%Y%m%d"), self.ice.name, self.tracers.name, self.currents.name)


def date_range(start_date, end_date):
    '''
    Generator that returns all dates from start_date to end_date inclusive
    '''
    for delta in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(delta)
