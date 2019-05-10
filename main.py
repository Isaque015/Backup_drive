import os
from shutil import copyfile

from setup_log import logger

path_home = os.environ['HOME']
path_dirs_local = '/Documents/livros/'
path_dirs_mega = '/megasync_up/livros/'
path_mega = path_home + '/megasync_up'

main_path_mega = path_home + path_dirs_mega
main_path = path_home + path_dirs_local

dirs_not_empty = [
    dirs for dirs in next(os.walk(main_path))[1]
    if not dirs.startswith('.') and len(os.listdir(main_path + dirs)) > 1
]


def check_mounted_mega(path_mega):

    if not os.path.exists(path_mega):
        logger.error('mega was not mounted or folder was excluded')
        return False
    return True


def check_dirs_empty(dirs_not_empty, main_path):

    if not os.path.exists(main_path):
        logger.error('pasta Livros não existe')
        return False

    if not dirs_not_empty:
        logger.error('Pasta livros está vazia')
        return False
    return True


def create_dirs_mega(main_path_mega, dirs_local_list, dirs_mega):

    if not dirs_mega:
        logger.error('mega was not mounted or folder was excluded')
        return False

    if not os.path.isdir(main_path_mega):
        os.mkdir(main_path_mega)
        logger.info(f'The folder {main_path_mega} was created.')

    logger_list_mv_folders = []
    for dirs in dirs_local_list:

        if os.path.exists(main_path_mega + '/' + dirs):
            continue

        os.mkdir(main_path_mega + '/' + dirs)
        logger_list_mv_folders.append(dirs)

    if logger_list_mv_folders:
        logger.info(
            f'the folders were created {logger_list_mv_folders} \
            \non the path {main_path_mega}.'
        )

    return True


def copy_files_mega(main_path_mega, dirs_not_empty, main_path):

    log_list_mv_files = []
    for dirs in dirs_not_empty:
        files_list = next(os.walk(main_path + dirs))[2]
        files_list_mega = os.listdir(main_path_mega + dirs)

        for files in files_list:

            if files in files_list_mega:
                continue

            copyfile(
                main_path + dirs + '/' + files,
                main_path_mega + dirs + '/' + files
            )

            log_list_mv_files.append(main_path_mega + dirs + '/' + files)

    if log_list_mv_files:
        logger.info(f'the files were created {log_list_mv_files}')
    return True


dirs_mega = check_mounted_mega(path_mega)
check = check_dirs_empty(dirs_not_empty, main_path)

if check and dirs_mega:
    result = create_dirs_mega(main_path_mega, dirs_not_empty, dirs_mega)
    if result:
        copy_files_mega(main_path_mega, dirs_not_empty, main_path)
