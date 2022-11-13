import rsa
from cryptography.fernet import Fernet

class CryptFile():

    def __init__(self, file_name, own_ip, server_ip):
        self.file_name = file_name
        self.own_ip = own_ip
        self.server_ip = server_ip
        self.public_key_server = None
        self.private_key = None
        self.symmetric_key = None


    def get_private_key(self):
        """Get the private key"""
         # to change to own_ip when we have the server
        with open(f'./{self.server_ip}/priv.key', 'rb') as key_file:
            self.private_key = key_file.read()

    def get_public_key_server(self):
        """Ask the server for his public key"""
        with open(f'{self.server_ip}/pub.key', 'rb') as key_file:
            self.public_key_server = key_file.read()
        
    def get_symmetric_key(self):
        """Get the symmetric key"""
        with open('./server1/sym.key', 'rb') as key_file:
            self.symmetric_key = key_file.read()

    def encrypt_file(self):
        """Encrypt the file"""
        with open(self.file_name, 'rb') as file:
            data_file = file.read()

        self.get_symmetric_key()
        cipher = Fernet(self.symmetric_key)
        encrypted_data = cipher.encrypt(data_file)

        with open(f'{self.file_name}.encrypted', 'wb') as file:
            file.write(encrypted_data)

        self.get_public_key_server() # TODO : get the ip of the server
        public_key_server = rsa.PublicKey.load_pkcs1(self.public_key_server)

        encrypted_symmetric_key = rsa.encrypt(self.symmetric_key, public_key_server)

        with open('./server1/encrypted_symmetric_key', 'wb') as file:
            file.write(encrypted_symmetric_key)

    def decrypt_file(self):
        """Decrypt the file"""
        self.get_private_key()
        private_key = rsa.PrivateKey.load_pkcs1(self.private_key)

        with open(f'./server1/encrypted_symmetric_key', 'rb') as file:
            encrypted_symmetric_key = file.read()

        self.symmetric_key = rsa.decrypt(encrypted_symmetric_key, private_key)

        with open(f'{self.file_name}.encrypted', 'rb') as file:
            encrypted_data = file.read()

        cipher = Fernet(self.symmetric_key)
        data_file = cipher.decrypt(encrypted_data)

        with open(f'decrypted_{self.file_name}', 'wb') as file:
            file.write(data_file)


        