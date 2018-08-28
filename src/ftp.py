import yaml


class FtpStorage:
    def __init__(self):
        self.dirs = self.init_directories()

    def init_directories(self):
        '''
        Deserialize directories from yaml-config to list of Directory objects
        '''
        config = self.load_config()

        dirs = []
        for dir in config['years']:
            dirs.append(Directory(dir['year'], dir['storage_ip'], dir['path']))

        return dirs

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


class Directory:
    def __init__(self, year, ip, path):
        self.year = year
        self.ip = ip
        self.path = path


storage = FtpStorage()
