import itertools

from src.ftp import FtpStorage
from src.name_format import NameFormat

storage = FtpStorage()
files = storage.get_results()

nf = NameFormat()

all_files = list(itertools.chain(*files))
print(len(all_files))

# for year in files:
#     for file in year:
#         print(file)
#         print(nf.match_type(file))
