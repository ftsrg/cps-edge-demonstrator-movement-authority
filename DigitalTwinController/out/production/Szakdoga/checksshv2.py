import paramiko
import sys
from paramiko.ssh_exception import SSHException,AuthenticationException,NoValidConnectionsError

def checkssh(ip,username,password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,username=username,password=password)
        print("Device is reachable")
    except AuthenticationException:
        print("Authentication failed, please verify your credentials")
    except NoValidConnectionsError as novalidException:
        print("Host is unreachable")
    finally:
        ssh.close()
checkssh(sys.argv[1],sys.argv[2],sys.argv[3])
