from cryptography.hazmat.primitives import serialization

from ._client import SatispayClient


def obtain_key_id(token, rsa_key, staging=False):
    target = '/g_business/v1/authentication_keys'
    key_encoding = serialization.Encoding.PEM
    key_format = serialization.PublicFormat.SubjectPublicKeyInfo
    public_key = rsa_key.public_key().public_bytes(key_encoding, key_format)
    body = {'public_key': public_key.decode(), 'token': token}
    with SatispayClient('PLACEHOLDER', rsa_key, staging) as client:
        return client.post(target, json=body)


def test_authentication(key_id, rsa_key):
    target = '/wally-services/protocol/tests/signature'
    headers = {'Content-Type': 'application/json'}
    with SatispayClient(key_id, rsa_key, True) as client:
        client.post(target, headers=headers)


def create_payment(key_id, rsa_key, amount_unit, currency, body_params=None, headers=None, staging=False):
    with SatispayClient(key_id, rsa_key, staging) as client:
        return client.create_payment(amount_unit, currency, body_params, headers)


def get_payment_details(key_id, rsa_key, payment_id, headers=None, staging=False):
    with SatispayClient(key_id, rsa_key, staging) as client:
        return client.get_payment_details(payment_id, headers)
