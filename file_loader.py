#load crestron config files over ftp
import ftplib
import os
import logging
from datetime import datetime
import argparse
import sys


def transfer_files(ftp_cli, paths):

    #transfer all files in list
    for path in paths:
        with open(path, 'rb') as file:
            ftp_cli.storbinary(f'STOR {path}', file)


def get_full_path(file_name):

    #get current directory of file
    cwd = os.path.dirname(os.path.realpath(__file__))
    #append file name to path
    return f'{cwd}\\{file_name}'


def check_if_files_exist(file_names):

    nonexistent_files = []
    for file in file_names:
        #if files to transfer do not exist return error msg
        if not os.path.exists(file):
            #return f'path specified for {file} does not exist'
            nonexistent_files.append(file)
    return nonexistent_files


def remove_non_existent_files(files, file_names, file_paths, logging):
    
    for file in files:
        if file in file_paths:
            index = file_paths.index(file)
            del file_names[index]
            del file_paths[index]
            print(f'File not found: {file}. Removing...')
            logging.warning(f'{datetime.now()}File not found: {file}. Removing...')


if __name__=='__main__':

    err = False
    logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG)

    #create command line parser object
    parser = argparse.ArgumentParser(prog='File Loader',description='IP Address of FTP Server and file names to transfer')
    parser.add_argument('--ip',type=str,help='ip of ftp server',required=True)
    parser.add_argument('--username',nargs='?',default='',type=str,help='username of ftp server')
    parser.add_argument('--password',nargs='?',default='',type=str,help='password of ftp server')
    parser.add_argument('files',nargs='+',type=str,help='names of files to transfer')
    parser.add_argument('--directory',nargs='?',default='USER',type=str,help='directory to transfer to')
    
    #parse command line args
    args = parser.parse_args()
    host = args.ip
    username = args.username
    password = args.password
    file_names = args.files
    directory = args.directory

    #apply full path to all files to transfer
    file_paths = list(map(get_full_path, file_names))
    #check if files exist
    file_check = check_if_files_exist(file_paths)

    if file_check != []:
        remove_non_existent_files(file_check, file_names, file_paths, logging)
    if file_names == []:
        logging.warning(f'No files to transfer. Exiting{"*"*100}')
        sys.exit('No files to transfer. Exiting...')

    try:
        #create ftp object
        ftp_client = ftplib.FTP(host)
        #if no username/password provided, login
        if(username == '' and password == ''):
            login_attempt = ftp_client.login()
        #login with provided username/password
        elif(username != '' and password != ''):
            login_attempt = ftp_client.login(username, password)

        logging.info(f'{datetime.now()}\nlogin attempted: {login_attempt}')
        #change working directory of ftp server to provided directory
        ftp_client.cwd(directory)

        #disable passive mode
        ftp_client.set_pasv(False)
        #transfer files
        transfer_files(ftp_client, file_names)
        ftp_client.close()

    except ftplib.all_errors as e:
        logging.exception(f'{datetime.now()}\nFTP Transfer Error {e.args}\n{"*"*100}')
        err = True
    except Exception as e:
        logging.exception(f'{datetime.now()}\nError {e.args}\n{"*"*100}')
        err = True

    if not err:
        for file in file_paths:
            logging.info(f'File successfully transferred: {file}')
            print(f'File successfully transferred: {file}')
        logging.info(f'{datetime.now()}\tFinished...\n{"*"*100}')
