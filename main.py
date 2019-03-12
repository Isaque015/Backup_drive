import os
from shutil import copyfile

from setup_log import logger

path_home = os.environ['HOME']
path_dirs_local = '/Documents/livros/'
path_dirs_drive = '/gdrive/Livros/'
path_gdrive = path_home + '/gdrive'

main_path_drive = path_home + path_dirs_drive
main_path = path_home + path_dirs_local

dirs_not_empty = [
    dirs for dirs in next(os.walk(main_path))[1]
    if not dirs.startswith('.') and len(os.listdir(main_path + dirs)) > 1
]


def check_mounted_gdrive(path_gdrive):

    dirs_drive = [
        dirs for dirs in os.listdir(path_gdrive) if not dirs.startswith('.')
    ]

    if not dirs_drive:
        logger.error('gdrive was not mounted or folder was excluded')
        return dirs_drive

    dirs_drive = True
    return dirs_drive


def check_dirs_empty(dirs_not_empty, main_path):

    if not os.path.exists(main_path):
        logger.error('pasta Livros não existe')
        return False

    if not dirs_not_empty:
        logger.error('Pasta livros está vazia')
        return False
    return True


def create_dirs_drive(main_path_drive, dirs_local_list, dirs_drive):

    if not dirs_drive:
        logger.error('gdrive was not mounted or folder was excluded')
        return False

    if not os.path.isdir(main_path_drive):
        os.mkdir(main_path_drive)
        logger.info(f'The folder {main_path_drive} was created.')

    logger_list_mv_folders = []
    for dirs in dirs_local_list:

        if os.path.exists(main_path_drive + '/' + dirs):
            continue

        os.mkdir(main_path_drive + '/' + dirs)
        logger_list_mv_folders.append(dirs)

    logger.info(
        f'the folders were created {logger_list_mv_folders} \
        \non the path {main_path_drive}.'
    )
    return True


def copy_files_drive(main_path_drive, dirs_not_empty, main_path):

    log_list_mv_files = []
    for dirs in dirs_not_empty:
        files_list = next(os.walk(main_path + dirs))[2]
        files_list_drive = next(os.walk(main_path_drive + dirs))[2]

        for files in files_list:

            if files in files_list_drive:
                continue

            copyfile(
                main_path + dirs + '/' + files,
                main_path_drive + dirs + '/' + files
            )

            log_list_mv_files.append(main_path_drive + dirs + '/' + files)
    logger.info(f'the files were created {log_list_mv_files}')
    return True


dirs_drive = check_mounted_gdrive(path_gdrive)
check = check_dirs_empty(dirs_not_empty, main_path)

if check and dirs_drive:
    result = create_dirs_drive(main_path_drive, dirs_not_empty, dirs_drive)
    if result:
        copy_files_drive(main_path_drive, dirs_not_empty, main_path)
