import sys
from datetime import date

from src.blade import BladeChecker

sys.path.append('/home/hpc-rosneft/nemo-error-checker/')

checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31))
checker.check_local_storage()
