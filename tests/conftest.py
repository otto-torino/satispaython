from pathlib import Path

from cryptography.hazmat.primitives import serialization
from pytest import fixture


@fixture(scope="session")
def rsa_key():
    path = Path(__file__).resolve().parent / "data/rsa_key.pem"
    with open(path, "rb") as file:
        return serialization.load_pem_private_key(file.read(), None)
