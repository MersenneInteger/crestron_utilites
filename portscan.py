#!/usr/bin/env python3
import socket
import subprocess
import sys
import os
import datetime

port_list = [21, 22, 23, 80, 8080, 443, 41794, 41795, 41796, 41797]
port_map = {21: 'FTP', 22: 'SSH', 23: 'Telnet', 80: 'HTTP', 8080: 'HTTP', 
            443: 'HTTPS', 41794: 'CIP', 41795: 'CTP', 41796: 'CIPS', 41797: 'CTPS'}

def validate_ip(ip):

    #split into 4 octets
    ip_list = ip.split('.')
    if len(ip_list) != 4:
        sys.exit('Error: invalid ip address: {0}\nCorrect format: xxx.xxx.xxx.xxx')
    #validate range of each octet
    for i in ip_list:
        if int(i) < 1 or int(i) > 254:
            sys.exit('Error: invalid ip address: {0}\nValid range 2-254')
    return True


def snip_last_octect(ip):

    #split octects into list
    ip_list = ip.split('.')
    #extract then delete last octet
    fourth_octect = ip_list[3]
    del ip_list[3]
    #join ip as str type and concat '.'
    ip_str = '.'.join(ip_list)
    ip_str = ip_str + '.'
    return fourth_octect, ip_str


def verify_os_and_build_ping(ip):

    #check for os type bc windows is assbackwards
    if sys.platform == 'linux' or sys.platform == 'darwin':
        cmd = ["ping", "-c", "3", ip]
    elif sys.platform == 'win32' and os.name == 'nt':
        cmd = ["ping", "-n", "1", ip]
    return cmd


def port_scan(ip, file_handle):

    try:             
        for port in port_list:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5) 
            result = sock.connect_ex((ip, port))
            if result == 0:
                file_handle.write(f'\t{port_map[port]} - {port} - OPEN\n')
            else:
                file_handle.write(f'\t{port_map[port]} - {port} - closed\n')
            sock.close()
    except Exception as err:
        print(err)
        raise


def main():

    #validate cli input
    if len(sys.argv) > 1 and len(sys.argv) < 4:

        start, stop = sys.argv[1], sys.argv[2]
        validate_ip(start)
        validate_ip(stop)
        start_host_bit, start = snip_last_octect(start)
        stop_host_bit, stop = snip_last_octect(stop)
        start_host_bit = int(start_host_bit)
        stop_host_bit = int(stop_host_bit)
       
        if stop_host_bit - start_host_bit >= 254:
            sys.exit('Error: keep host bit range between 2-254 or it will take all day')
        if start_host_bit >= stop_host_bit:
            sys.exit('Error: invalid ip range, make sure first argument is less than the second')
    else:
        sys.exit('Error: invalid number of arguments\nCorrect format [script] ip1 ip2')
        
    try:
        with open('scan_result.txt', 'w') as file_handle:

            tod = datetime.datetime.today()
            file_handle.write(f'{tod}\n\n')

            for ip in range(start_host_bit, stop_host_bit+1):
                
                new_ip = start + str(ip)
                #check os type, ping works different on windows vs linux
                cmd = verify_os_and_build_ping(new_ip)
                #ping host
                ping = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                host_alive, err = ping.communicate()
                host_alive = host_alive.decode()

                if 'host unreachable' in host_alive or 'Host Unreachable' in host_alive:
                    print(f'{new_ip}-Host unreachable')
                    file_handle.write(f'{new_ip}-Host unreachable\n')
                    continue
                else:
                    print(f'{new_ip}-Host alive')
                    file_handle.write(f'{new_ip}-Host alive\n')

                #scan ip for open ports specified in ports_list
                port_scan(new_ip, file_handle)

    except Exception as e:
        print('Error: {}'.format(e.args()))

if __name__ == '__main__':
    main()
