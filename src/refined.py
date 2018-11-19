from datetime import date

from src.blade import BladeChecker
from src.file_format import FileFormat

# checker = BladeChecker(date_from=date(2004, 1, 1), date_to=date(2008, 12, 31),
#                        file_format=FileFormat(format_file="../formats/nemo14-formats.yaml"))
# checker.check_local_storage(mode="", summary=True)

# storage = FtpStorage()
# checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31))
# checker.check_storage_with_ftp(storage, mode='absence', summary=True)

# checker = BladeChecker(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31),
#                       file_format=FileFormat(format_file='../formats/wrf-formats.yaml'))
# checker.check_wrf_files(mode='', summary=True)

checker = BladeChecker(date_from=date(1965, 1, 1), date_to=date(2015, 12, 31),
                       file_format=FileFormat(format_file='../formats/ww3-formats.yaml'))
checker.check_wave_watch_files(mode='absence', summary=True)
