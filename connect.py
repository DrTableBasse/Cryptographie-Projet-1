# Connect to the server and get the public key of the server /etc/rsa_keys/pub.key
import paramiko

def connect(ip, user, password):
    """Connect to the server"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password)
    return ssh

def get_public_key_server(ssh):
    """Get the public key of the server"""
    sftp = ssh.open_sftp()
    sftp.get('/etc/rsa_keys/pub.key', 'pub.key')
    sftp.close()

def get_symmetric_key(ssh):
    """Get the symmetric key"""
    sftp = ssh.open_sftp()
    sftp.get('/etc/rsa_keys/sym.key', 'sym.key')
    sftp.close()




