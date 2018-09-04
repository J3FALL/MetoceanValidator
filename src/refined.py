from datetime import date

from src.blade import BladeChecker

checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(1965, 1, 1))
checker.check_local_storage(mode="vars")
