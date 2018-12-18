#!/usr/bin/env python3
import socket, subprocess, sys

if len(sys.argv) > 1:
    ip_range = (int(sys.argv[1]), int(sys.argv[2]))
else:
    ip_range = (2, 255)

def main():

    class_c_mask = '192.168.1.'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            
            sock.settimeout(1) 
            file_handle = open('scan_result.txt', 'w')

            for ip in range(*ip_range):
                
                new_ip = class_c_mask + str(ip)
                ping = subprocess.Popen(['ping','-c','2',new_ip],
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)
                host_alive, err = ping.communicate()
                host_alive = host_alive.decode()

                if 'Host Unreachable' in host_alive:
                    print(f'{new_ip}-Host unreachable')
                    file_handle.write(f'{new_ip}-Host unreachable\n')
                else:
                    print(f'{new_ip}-Host alive')
                    file_handle.write(f'{new_ip}-Host alive\n')

                    for port in range(41794, 41796):
                        result = sock.connect_ex((new_ip, port))
                        if result == 0:
                            file_handle.write(f'\t{port} open\n')
                        else:
                            file_handle.write(f'\t{port} closed\n')
        file_handle.close()

    except Exception as e:
        print('Error: {}'.format(e.args()))

if __name__ == '__main__':
    main()
