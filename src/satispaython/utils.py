from cryptography.hazmat.primitives import serialization as _serialization
from cryptography.hazmat.primitives.asymmetric import rsa as _rsa


def generate_key():
    return _rsa.generate_private_key(65537, 4096)


def write_key(key, path, password=None):
    if password:
        password = password.encode()
        encryption_algorithm = _serialization.BestAvailableEncryption(password)
    else:
        encryption_algorithm = _serialization.NoEncryption()
    pem = key.private_bytes(_serialization.Encoding.PEM, _serialization.PrivateFormat.PKCS8, encryption_algorithm)
    with open(path, 'wb') as file:
        file.write(pem)


def load_key(path, password=None):
    if password:
        password = password.encode()
    with open(path, 'rb') as file:
        return _serialization.load_pem_private_key(file.read(), password)


def format_datetime(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
