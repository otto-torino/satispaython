from pathlib import Path

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from pytest import fixture


@fixture(scope="session")
def rsa_key():
    path = Path(__file__).resolve().parent / "data/rsa_key.pem"
    with open(path, "rb") as file:
        return load_pem_private_key(file.read(), None)
