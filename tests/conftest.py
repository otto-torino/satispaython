from pytest import fixture
from cryptography.hazmat.primitives import serialization


@fixture(scope='session')
def key():
    with open('key.pem', 'rb') as file:
        return serialization.load_pem_private_key(file.read(), None)
