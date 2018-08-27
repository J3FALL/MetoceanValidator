from src.valid import ValidResults


class Experiment:
    def __init__(self, date_from, date_to):
        self._date_from = date_from
        self._date_to = date_to
        self._results_by_day = []

    def check_for_absence(self):
        '''
        Check whether results contain all days and each day contains
        three corresponding resulted files: [ice, tracers, currents]
        :return:
        '''

        raise NotImplementedError
        valid_results = ValidResults().generate(self._date_from, self._date_to)

        assert len(self._results_by_day) == len(valid_results)

        for valid, given in zip(valid_results, self._results_by_day):
            print(valid, given)
