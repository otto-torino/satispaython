from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=4096)


def write_key(key, path, password=None):
    if password:
        password = password.encode('utf-8')
        encryption_algorithm = serialization.BestAvailableEncryption(password) 
    else:
        encryption_algorithm = serialization.NoEncryption()
    pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=encryption_algorithm)
    with open(path, 'wb') as file:
        file.write(pem)


def load_key(path, password=None):
    if password:
        password = password.encode('utf-8')
    with open(path, "rb") as file:
        return serialization.load_pem_private_key(file.read(), password)