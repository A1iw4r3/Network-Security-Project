from argparse import ArgumentParser
import socket
from threading import Thread
from time import time
open_port=[]
def prepare_arg():
    parser=ArgumentParser(description="Python based Fast Ports scanner", usage="%(prog)s 192.168.1.2",epilog="Example - %(prog)s -s 20 -e 4000 -t 500 -v")
    parser.add_argument(metavar='IPv4',dest="ip",help='host to scan')
    parser.add_argument("-s","--start",dest="start",metavar='\b',type=int,help="starting port",default=1)
    parser.add_argument('-e','--end',dest='end',metavar='\b',type=int,help="ending port",default=1000)
    parser.add_argument('-t','--threads',dest='thread',metavar='\b',type=int,help="threads to use",default=500)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true',help='verbose output')
    parser.add_argument('-V','--version',dest='version',action='version',version='%(prog)s 1.0',help='Display version')
    arguments=parser.parse_args()
    return arguments
def prep_port(start:int,end:int):
    for ports in range(start,end+1):
        yield ports
def prep_thread(thread:int):
    thread_list=[]
    for _ in range(thread+1):
        thread_list.append(Thread(target=scan_port))
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
def scan_port():
    while True:
        try:
            s=socket.socket()
            s.settimeout(1)
            port=next(ports)
            s.connect((arguments.ip,port))
            open_port.append(port)
            if arguments.verbose:
                print(f'\r{open_port}',end='')
        except(ConnectionRefusedError,socket.timeout):
            continue
        except StopIteration:
            break                
if __name__ == "__main__":
    arguments=prepare_arg()
    ports=prep_port(arguments.start,arguments.end)
    start_time=time()
    threads=prep_thread(arguments.thread)
    end_time=time()
    print(f"\nOpen Ports Found - {open_port}")
    if arguments.verbose:
        print()
        print(f'Time taken - {round(end_time-start_time,3)}')