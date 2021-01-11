from cryptography.hazmat.primitives import serialization
from satispaython._core import send_request


def obtain_key_id(key, token, staging=False):
    target = '/g_business/v1/authentication_keys'
    public_pem = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    body = {'public_key': public_pem.decode(), 'token': token}
    return send_request(None, None, 'post', target, body, None, staging)


def test_authentication(key_id, key):
    target = '/wally-services/protocol/tests/signature'
    return send_request(key_id, key, 'post', target, None, None, True)


def create_payment(key_id, key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None, staging=False):
    target = '/g_business/v1/payments'
    body = {'flow': 'MATCH_CODE', 'amount_unit': amount_unit, 'currency': currency, 'callback_url': callback_url}
    if expiration_date:
        body.update({'expiration_date': expiration_date})
    if external_code:
        body.update({'external_code': external_code})
    if metadata:
        body.update({'metadata': metadata})
    return send_request(key_id, key, 'post', target, body, idempotency_key, staging)


def get_payment_details(key_id, key, payment_id, staging=False):
    target = f'/g_business/v1/payments/{payment_id}'
    return send_request(key_id, key, 'get', target, None, None, staging)
