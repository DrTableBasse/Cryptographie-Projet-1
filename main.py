"""
python main.py file1
chiffré le file1 avec la clé publique du serveur2
envoyer le file1 chiffré au serveur2

dechiffré le file1 avec la clé privée du serveur2
"""

import os
import argparse

from crypt_file import CryptFile
from generate_key import generate_symmetric_key, generate_public_key, generate_private_key


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file.')
    parser.add_argument('file_name', help='The file to encrypt or decrypt.')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt the file.')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt the file.')
    args = parser.parse_args()


    # path_of_keys = None # TODO : get the path of the keys on the server

    # Generate the keys if they don't exist    
    if not all(os.path.exists(f'.server1/{f_name}') for f_name in ['pub.key', 'priv.key', 'sym.key']):
        generate_symmetric_key()
        generate_public_key()
        generate_private_key()

    # ip_server1 = None # TODO : get the ip of the server
    # ip_server2 = None # TODO : get the ip of the server
    
    crypt_file = CryptFile(args.file_name, "server1", "server2")

    if args.encrypt:
        crypt_file.encrypt_file()
    elif args.decrypt:
        crypt_file.decrypt_file()