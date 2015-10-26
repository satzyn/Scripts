from multiprocessing import Array
from multiprocessing.dummy import Pool as ThreadPool
import time
import paramiko
from colorama import init
from colorama import Fore, Back, Style

def processFunc(hostname):
    cmds = str( "yum update -y")

    #print(Fore.WHITE + 'Working on VM' + hostname )
    handle = paramiko.SSHClient()
    handle.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        handle.connect(hostname,22, username='root', password='Password')
        stdin, stdout, stderr = handle.exec_command(cmds)
        cmdOutput = ""
        while True:
            try:
                cmdOutput += stdout.next()
            except StopIteration:
                break
        handle.close()
        #print(Fore.WHITE + "Finished ...!" )
        return('VM' + hostname + ':' + cmdOutput)
    except paramiko.AuthenticationException:
        return('VM' + hostname + ':' "Invalid Password")
    except socket.error, e:
        return('VM' + hostname + ':' "Comunication problem")

if __name__ == '__main__':
    pool = ThreadPool(10)
    with open('vms.txt') as infile:
        vmnames = infile.read().splitlines()
        #print vmnames
        results = pool.map(processFunc,vmnames)
        pool.close()
        pool.join()
    #print Fore.GREEN + '\n'.join(results)
