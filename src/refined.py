from datetime import date

from src.blade import BladeChecker
from src.ftp import FtpStorage
from src.ftp import download_missed_files

# checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31))
# checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(1965, 1, 1))
# checker.check_local_storage(mode="")

storage = FtpStorage()
download_missed_files(storage)