from cryptography.hazmat.primitives.asymmetric import rsa as _rsa
from cryptography.hazmat.primitives import serialization as _serialization


def generate_key():
    return _rsa.generate_private_key(public_exponent=65537, key_size=4096)


def write_key(key, path, password=None):
    if password:
        password = password.encode('utf-8')
        encryption_algorithm = _serialization.BestAvailableEncryption(password) 
    else:
        encryption_algorithm = _serialization.NoEncryption()
    pem = key.private_bytes(encoding=_serialization.Encoding.PEM, format=_serialization.PrivateFormat.PKCS8, encryption_algorithm=encryption_algorithm)
    with open(path, 'wb') as file:
        file.write(pem)


def load_key(path, password=None):
    if password:
        password = password.encode('utf-8')
    with open(path, "rb") as file:
        return _serialization.load_pem_private_key(file.read(), password)


def format_datetime(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'