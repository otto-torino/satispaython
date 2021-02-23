from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from .client import SatispayClient
from httpx import Response, Headers
from typing import Optional


def obtain_key_id(token: str, rsa_key: RSAPrivateKey, staging: bool = False) -> Response:
    target = '/g_business/v1/authentication_keys'
    key_encoding = Encoding.PEM
    key_format = PublicFormat.SubjectPublicKeyInfo
    public_key = rsa_key.public_key().public_bytes(key_encoding, key_format)
    body = {'public_key': public_key.decode(), 'token': token}
    with SatispayClient('PLACEHOLDER', rsa_key, staging) as client:
        return client.post(target, json=body)


def test_authentication(key_id: str, rsa_key: RSAPrivateKey) -> Response:
    target = '/wally-services/protocol/tests/signature'
    headers = {'Content-Type': 'application/json'}
    with SatispayClient(key_id, rsa_key, True) as client:
        return client.post(target, headers=headers)


def create_payment(
    key_id: str,
    rsa_key: RSAPrivateKey,
    amount_unit: int,
    currency: str,
    body_params: Optional[dict] = None,
    headers: Optional[Headers] = None,
    staging: bool = False
) -> Response:
    with SatispayClient(key_id, rsa_key, staging) as client:
        return client.create_payment(amount_unit, currency, body_params, headers)


def get_payment_details(
    key_id: str,
    rsa_key: RSAPrivateKey,
    payment_id: str,
    headers: Optional[Headers] = None,
    staging: bool = False
) -> Response:
    with SatispayClient(key_id, rsa_key, staging) as client:
        return client.get_payment_details(payment_id, headers)
