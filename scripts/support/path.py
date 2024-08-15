import os

__root_project = os.getcwd()
while not os.path.basename(__root_project) == 'Ebbinghaus':
    __root_project = os.path.split(__root_project)[0]


def get_path_to_database():
    return os.path.join(__root_project, 'DataBase', 'Ebbinghaus.db')


def get_path_to_file_temp(name_file):
    return os.path.join(__root_project, 'temp', name_file)
