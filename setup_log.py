import logging
import logging.config

try:
    logging.config.fileConfig('conf_log.ini')
except FileNotFoundError:
    # se a pasta ou o arquivo que serão armazenados os logs não existir
    from configparser import ConfigParser
    from os import makedirs

    config = ConfigParser()
    config.read('conf_log.ini')

    dir_file_key = dict(config['handler_FileHandler'])
    path_dir_file = eval(dir_file_key['args'])[0]

    path_without_file = path_dir_file.split('/')[:-1]

    path_create_dir = str(
        path_without_file
    ).replace("', '", "/").lstrip("[").rstrip("']").lstrip("'")

    makedirs(path_create_dir)

    logging.config.fileConfig('conf_log.ini')

logger = logging.getLogger('root')
