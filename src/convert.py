from src.ftp import FtpStorage
from src.name_format import NameFormat

storage = FtpStorage()
files = storage.get_results()

nf = NameFormat()

for file in files[0]:
    print(file)
    print(nf.match_type(file))
