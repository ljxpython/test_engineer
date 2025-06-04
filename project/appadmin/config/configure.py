import configparser


class Configure:
    __config_file = r'C:\Users\86134\Desktop\workspace\HCPlaywright-public\appadmin\config\config.ini'

    def __init__(self):
        c = configparser.ConfigParser()
        c.read(Configure.__config_file)
        self.__repository_path = c.get('repository', 'repository_path')

    @property
    def repository_path(self):
        return self.__repository_path


# 初始化配置文件信息，只执行一次
config = Configure()
