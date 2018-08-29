from datetime import date

from src.experiment import Experiment
from src.ftp import FtpStorage

storage = FtpStorage()
files = storage.get_results()

exp = Experiment(date_from=date(1964, 1, 1), date_to=date(2015, 12, 31), resulted_files=files)

errors = exp.check_for_absence()

print(errors)
