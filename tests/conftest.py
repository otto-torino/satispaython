from pytest import fixture
from pathlib import Path
from cryptography.hazmat.primitives import serialization


@fixture(scope='session')
def key():
    path = Path(__file__).resolve().parent / 'data/key.pem'
    with open(path, 'rb') as file:
        return serialization.load_pem_private_key(file.read(), None)
