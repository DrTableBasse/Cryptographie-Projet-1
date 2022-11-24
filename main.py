import os, sys
import argparse

from box_log import log
from crypt_file import CryptFile
from generate_key import generate_symmetric_key, generate_public_key, generate_private_key
from connect import stored_path, send_path, user, host

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file.')
    parser.add_argument('file_name', help='The file to encrypt or decrypt.')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt the file.')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt the file.')
    args = parser.parse_args()


    # Generate the keys if they don't exist    
    if not all(os.path.exists(f'/etc/rsa_keys/{f_name}') for f_name in ['pub.key', 'priv.key', 'sym.key']):
        generate_symmetric_key()
        generate_public_key()
        generate_private_key()
        log("Keys generated", "Path: /etc/rsa_keys")
        sys.exit(0)

    
    crypt_file = CryptFile(args.file_name)

    if args.encrypt:
        # crypt_file.save_hash()
        crypt_file.encrypt_file()
        log("File encrypted", f"Path: {stored_path}{args.file_name}.encrypted")
        os.system(f"scp {stored_path}* {user}@{host}:{send_path}")
        log("File sent", f"Path: {send_path}")

    elif args.decrypt:
        # print("decrypt file")
        crypt_file.decrypt_file()
        log("File decrypted", f"Path: {args.file_name}.decrypted")
        # print("hash file et vérifier qu'il est le même que celui écrit à la fin du fichier")
        # crypt_file.check_hash()
        # log("File decrypted", f"Path: {args.file_name}")
        # log("Hash verified", f"Hash: {crypt_file.hash_file()}")
