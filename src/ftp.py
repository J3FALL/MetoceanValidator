import ftplib
import os

import yaml
from tqdm import tqdm


class FtpStorage:
    def __init__(self):
        self.storages, self.storage_to_dirs = self.init_storages()
        self.dirs = self.init_directories()
        self.credentials = self.init_credentials()

    def init_directories(self):
        '''
        Deserialize directories from yaml-config to list of Directory objects
        '''
        config = self.load_config()

        dirs = []
        for dir in config['years']:
            dirs.append(Directory(dir['year'], dir['storage_ip'], dir['path']))

        return dirs

    def init_storages(self):
        config = self.load_config()
        storages = []
        storage_to_dirs = {}

        for storage in config['storages']:
            storages.append(storage['ip'])
            storage_to_dirs[storage['ip']] = storage['mount_dir']

        return storages, storage_to_dirs

    def init_credentials(self):
        config = self.load_config()
        return config['credentials']

    def load_config(self):
        '''
        Load yaml-config file containing the list of all directories for each simulation year
        :return: directories as dictionary
        '''
        with open("../ftp-config.yaml") as stream:
            try:
                loaded = yaml.load(stream)
                return loaded
            except yaml.YAMLError as exc:
                print(exc)

    def get_results(self):
        '''
        :return: List of all simulation results
        '''
        connects = dict()
        for storage in self.storages:
            connects[storage] = ftplib.FTP(host=storage, user=self.credentials['user'], passwd=self.credentials['pass'])

        files = []
        for dir in self.dirs:
            print("year: %s" % dir.year)
            connect = connects[dir.ip]
            try:
                connect.cwd(dir.path)
                files.append(connect.nlst())
            except Exception:
                print("error has occurred")

        return files

    def download_year(self, year, path_to_download=''):

        dir = next(d for d in self.dirs if d.year == year)
        connect = ftplib.FTP(host=dir.ip, user=self.credentials['user'], passwd=self.credentials['pass'])

        files = []
        try:
            connect.cwd(dir.path)
            files = connect.nlst()
        except Exception:
            print("error has occurred")

        for file in tqdm(files):
            host_file = os.path.join(path_to_download, file)
            with open(host_file, 'wb') as local_file:
                connect.retrbinary('RETR ' + file, local_file.write)


class Directory:
    def __init__(self, year, ip, path):
        self.year = year
        self.ip = ip
        self.path = path


def missed_years(ftp_storage):
    missed = []
    for dir in ftp_storage.dirs:
        full_path = os.path.join(ftp_storage.storage_to_dirs[dir.ip], dir.path)

        if not os.path.exists(full_path):
            missed.append(dir.year)

    return missed


def download_missed_files(ftp_storage, temp_dir="../temp_missed/"):
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    missed_years_ = missed_years(ftp_storage)
    for dir in ftp_storage.dirs:
        if dir.year in missed_years_:
            ftp_storage.download_year(dir.year, path_to_download=temp_dir)
