#!/usr/bin/env python3
import socket, subprocess, sys, os

def validateIP(ip):

    #split into 4 octets
    ip_list = ip.split('.')
    if len(ip_list) != 4:
        sys.exit('Error: invalid ip address: {0}\nCorrect format: xxx.xxx.xxx.xxx')
    #validate range of each octet
    for i in ip_list:
        if int(i) < 1 and int(i) > 254:
            sys.exit('Error: invalid ip address: {0}\nValid range 2-254')
            return False
    return True

def snipLastOctect(ip):

    ip_list = ip.split('.')
    fourth_octect = ip_list[3]
    del ip_list[3]
    ip_str = '.'.join(ip_list)
    ip_str = ip_str + '.'
    return fourth_octect, ip_str

if len(sys.argv) > 1 and len(sys.argv) < 4:
        
    start, stop = sys.argv[1], sys.argv[2]
    validateIP(start)
    validateIP(stop)
    start_host_bit, start = snipLastOctect(start)
    stop_host_bit, stop = snipLastOctect(stop)
    start_host_bit = int(start_host_bit)
    stop_host_bit = int(stop_host_bit)
    
    if stop_host_bit - start_host_bit >= 254:
        sys.exit('Error: keep host bit range between 2-254 or it will take all day')
    if start_host_bit >= stop_host_bit:
        sys.exit('Error: invalid ip range, make sure first argument is less than the second')
else:
    sys.exit('Error: invalid number of arguments\nCorrect format [script] ip1 ip2')

def main():

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            
            sock.settimeout(1) 
            file_handle = open('scan_result.txt', 'w')

            for ip in range(start_host_bit, stop_host_bit+1):
                
                new_ip = start + str(ip)

                ping = subprocess.Popen(['ping','-c','2',new_ip],
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)
                host_alive, err = ping.communicate()
                host_alive = host_alive.decode()

                print(ping.stdout, ping.stderr)

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
