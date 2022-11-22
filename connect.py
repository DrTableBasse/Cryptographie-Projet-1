# Connect to the server and get the public key of the server /etc/rsa_keys/pub.key
import json
import paramiko

def connect_server(ip, user, password, port):
    """Connect to the server"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, password)
    return ssh


def get_file(ssh, path, file_name):
    """Get the file from the server and return the contents of it"""
    sftp = ssh.open_sftp()
    sftp.get(f'{path}/{file_name}', file_name)
    with open(file_name, 'rb') as file:
        data = file.read()
    return data

def read_config_file():
    """Read the config file"""
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

"""
Variables
"""

host, port, user, pwd, stored_path, send_path = read_config_file().values()