import ftplib
import os
import logging
from datetime import datetime
import argparse
import sys

def load_file(ftp_cli, paths):

    for path in paths:
        with open(path, 'rb') as file:
            ftp_cli.storbinary(f'STOR {path}', file)


def get_full_path(file_name):

    cwd = os.path.dirname(os.path.realpath(__file__))
    return f'{cwd}\\{file_name}'


def check_if_files_exist(file_names):

    for file in file_names:
        if not os.path.exists(file):
            return f'path specified for {file} does not exist'
    return None


if __name__=='__main__':

    logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('ip',type=str,help='ip of ftp server')
    parser.add_argument('files',nargs='+',type=str,help='names of files to transfer')
    
    args = parser.parse_args()
    host = args.ip
    file_names = args.files

    file_paths = list(map(get_full_path, file_names))
    file_check = check_if_files_exist(file_paths)
    if file_check is not None:
        logging.error(f'{file_check}\nexiting...\n{"*"*100}')
        sys.exit()

    try:
        ftp_client = ftplib.FTP(host)
        login_attempt = ftp_client.login()
        logging.info(f'login attempted: {login_attempt}')
        ftp_client.cwd('USER')

        load_file(ftp_client, file_paths)
        ftp_client.quit()

    except ftplib.all_errors as e:
        logging.exception(f'{datetime.now()}\nFTP Transfer Error {e.args}\n{"*"*100}')
    except Exception as e:
        logging.exception(f'{datetime.now()}\nError {e.args}\n{"*"*100}')

    logging.info(f'{datetime.now()}\tFinished...\n{"*"*100}')
