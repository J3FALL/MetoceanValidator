from src.valid import ValidResults


class Experiment:
    def __init__(self, date_from, date_to, results_by_days):
        self._date_from = date_from
        self._date_to = date_to
        self._results_by_days = results_by_days
        self._results_by_days.sort(key=lambda day: day.date)

    def check_for_absence(self):
        '''
        Check whether results contain all days and each day contains
        three corresponding resulted files: [ice, tracers, currents]
        :return: False if all resulted files are presented, otherwise exceptions were raised
        '''

        valid_results = ValidResults().generate(self._date_from, self._date_to)

        for valid, given in zip(valid_results, self._results_by_days):
            if valid.date != given.date:
                error = "Simulation results were not found for day: %s" % valid.date.strftime("%Y%m%d")
                raise Exception(error)
            elif valid != given:
                error = "Simulation results for day: %s have some missing files or its names are incorrect: %s" % \
                        (valid.date.strftime("%Y%m%d"), given)
                raise Exception(error)

        return False
