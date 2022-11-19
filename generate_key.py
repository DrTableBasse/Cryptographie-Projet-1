import rsa
from cryptography.fernet import Fernet

# Create a public/private key pair
(pulic_key, private_key) = rsa.newkeys(2048)

def generate_symmetric_key():
    """Generate a symmetric key"""
    key = Fernet.generate_key()
    with open('/etc/rsa_keys/sym.pub', 'wb') as key_file:
        key_file.write(key)

def generate_public_key():
    """Generate a public key"""
    with open('/etc/rsa_keys/pub.key', 'wb') as key_file:
        key_file.write(pulic_key.save_pkcs1('PEM'))

def generate_private_key():
    """Generate a private key"""
    with open('/etc/rsa_keys/priv.key', 'wb') as key_file:
        key_file.write(private_key.save_pkcs1('PEM'))