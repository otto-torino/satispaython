from datetime import datetime
from contextlib import suppress
from os import PathLike
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    generate_private_key,
)
from cryptography.hazmat.primitives.serialization import (
    BestAvailableEncryption,
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_pem_private_key,
)


def generate_key(
    path: Optional[PathLike] = None, password: Optional[str] = None
) -> RSAPrivateKey:
    rsa_key = generate_private_key(65537, 4096)
    if path:
        write_key(rsa_key, path, password)
    return rsa_key


def write_key(
    rsa_key: RSAPrivateKey, path: PathLike, password: Optional[str] = None
) -> None:
    try:
        encryption_algorithm = BestAvailableEncryption(password.encode())
    except AttributeError:
        encryption_algorithm = NoEncryption()
    pem = rsa_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, encryption_algorithm)
    with open(path, "wb") as file:
        file.write(pem)


def load_key(path: PathLike, password: Optional[str] = None) -> RSAPrivateKey:
    with suppress(AttributeError):
        password = password.encode()
    with open(path, "rb") as file:
        return load_pem_private_key(file.read(), password)


def format_datetime(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
