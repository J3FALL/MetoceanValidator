import ftplib

import yaml


class FtpStorage:
    def __init__(self):
        self.storages = self.init_storages()
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
        return [storage for storage in config['storages']]

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


class Directory:
    def __init__(self, year, ip, path):
        self.year = year
        self.ip = ip
        self.path = path
