from datetime import date

from src.blade import BladeChecker
from src.file_format import FileFormat

checker = BladeChecker(date_from=date(1974, 1, 1), date_to=date(2015, 12, 31),
                       file_format=FileFormat(format_file="../formats/reduced-nemo14.yaml"),
                       storage_path='/home/rosneft_user_2500/nfs/31/NEMO-ARCT/coarse_grid/',
                       log_file_path='../logs/errors.log')
checker.check_nemo_files(mode='absence', summary=True)
