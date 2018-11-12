from datetime import date

from src.blade import BladeChecker
from src.ftp import FtpStorage

# checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31))
# checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(1965, 1, 1))
# checker.check_local_storage(mode="")

storage = FtpStorage()
checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31))
checker.check_storage_with_ftp(storage, mode='absence', summary=True)
