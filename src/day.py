from datetime import timedelta


class ExperimentDay:
    def __init__(self, date, ice_file=None, tracers_file=None, currents_file=None):
        self.date = date
        self.ice = ice_file
        self.tracers = tracers_file
        self.currents = currents_file

    def is_none(self):
        return self.ice is None and self.tracers is None and self.currents is None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.date == other.date and self.ice == other.ice and \
                   self.tracers == other.tracers and \
                   self.currents == other.currents
        return False

    def __ne__(self, other):
        return self.date != other.date or self.ice != other.ice or \
               self.tracers != other.tracers or \
               self.currents != other.currents

    def __str__(self):
        return "date: %s, ice_file: %s, tracers_file: %s, currents_file: %s" % \
               (self.date.strftime("%Y%m%d"), self.ice, self.tracers, self.currents)


def date_range(start_date, end_date):
    '''
    Generator that returns all dates from start_date to end_date inclusive
    '''
    for delta in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(delta)
