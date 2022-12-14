import rsa
from cryptography.fernet import Fernet
from connect import connect_server, get_file
from box_log import log_error
from connect import host, port, user, pwd, stored_path, send_path

class CryptFile():

    def __init__(self, file_name:str):
        self.file_name = file_name
        self.public_key_server = None
        self.private_key = None
        self.symmetric_key = None


    def get_private_key(self):
        """Get the private key"""
         # to change to own_ip when we have the server
        with open(f'/etc/rsa_keys/priv.key', 'rb') as key_file:
            self.private_key = key_file.read()

    def get_public_key_server(self):
        """Ask the server for his public key"""
        ssh = connect_server(host, user, pwd, port)
        self.public_key_server = get_file(ssh, "/etc/rsa_keys/", "pub.key")
        
    def get_symmetric_key(self):
        """Get the symmetric key"""
        with open('/etc/rsa_keys/sym.key', 'rb') as key_file:
            self.symmetric_key = key_file.read()

    def encrypt_file(self):
        """Encrypt the file"""

        # Read the file
        with open(self.file_name, 'rb') as file:
            data_file = file.read()

        # Get the symmetric key and create the cipher to encrypt the file
        self.get_symmetric_key()
        cipher = Fernet(self.symmetric_key)
        encrypted_data = cipher.encrypt(data_file)

        # Save the encrypted file
        with open(f'{stored_path}{self.file_name}.encrypted', 'wb') as file:
            file.write(encrypted_data)

        # Get the public key of the server that will receive the file
        self.get_public_key_server()
        public_key_server = rsa.PublicKey.load_pkcs1(self.public_key_server)

        # Encrypt the symmetric key
        encrypted_symmetric_key = rsa.encrypt(self.symmetric_key, public_key_server)

        # Save the encrypted symmetric key
        with open('/etc/rsa_keys/encrypted_symmetric_key', 'wb') as file:
            file.write(encrypted_symmetric_key)

        return True

    def decrypt_file(self):
        """Decrypt the file"""

        # Get the private key
        self.get_private_key()
        private_key = rsa.PrivateKey.load_pkcs1(self.private_key)

        # Get the encrypted symmetric key from the server that sent the file
        ssh = connect_server(host, user, pwd, port)
        encrypted_symmetric_key = get_file(ssh, '/etc/rsa_keys/', 'encrypted_symmetric_key')

        # Decrypt the symmetric key
        self.symmetric_key = rsa.decrypt(encrypted_symmetric_key, private_key)

        # Get the encrypted file
        with open(f'./{self.file_name}', 'rb') as file:
            encrypted_data = file.read()

        # Decrypt the file
        cipher = Fernet(self.symmetric_key)
        try:
            data_file = cipher.decrypt(encrypted_data)
        except Exception:
            return False

        # Save the decrypted file
        with open(f'decrypted_{self.file_name}', 'wb') as file:
            file.write(data_file)

        return True
    

