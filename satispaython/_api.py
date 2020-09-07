from satispaython._core import send_request
from cryptography.hazmat.primitives import serialization

def obtain_key_id(key, token, staging=False):
    target = '/g_business/v1/authentication_keys'
    public_pem = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    public_pem = public_pem.decode('utf-8')
    body = { 'public_key': public_pem, 'token': token }
    return send_request(None, None, 'post', target, body, None, staging)


def test_authentication(key_id, key):
    target = '/wally-services/protocol/tests/signature'
    body = { 'flow': 'MATCH_CODE', 'amount_unit': 100, 'currency': 'EUR' }
    return send_request(key_id, key, 'post', target, body, None, True)


def create_payment(key_id, key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None, staging=False):
    target = '/g_business/v1/payments'
    body = { 'flow': 'MATCH_CODE', 'amount_unit': amount_unit, 'currency': currency, 'callback_url': callback_url }
    if external_code:
        body = { **body, 'external_code': external_code }
    if metadata:
        body = { **body, 'metadata': metadata }
    if expiration_date:
        body = { **body, 'expiration_date': expiration_date }
    return send_request(key_id, key, 'post', target, body, idempotency_key, staging)


def get_payment_details(key_id, key, payment_id, staging=False):
    target = f'/g_business/v1/payments/{payment_id}'
    return send_request(key_id, key, 'get', target, None, None, staging)