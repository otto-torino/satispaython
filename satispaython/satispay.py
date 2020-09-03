from satispaython.core import send_request
from cryptography.hazmat.primitives import serialization


def obtain_key_id(key, token, staging=False):
    target = '/g_business/v1/authentication_keys'
    public_pem = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    public_pem = public_pem.decode('utf-8').strip().replace('\n', '\\n')
    body = '{ "public_key": "%s", "token": "%s" }' % (public_pem, token)
    return send_request(None, None, 'post', target, body, None, staging)


def test_authentication(key_id, key):
    target = '/wally-services/protocol/tests/signature'
    body = '{ "flow": "MATCH_CODE", "amount_unit": 100, "currency": "EUR"}'
    return send_request(key_id, key, 'post', target, body, None, True)


def create_payment(key_id, key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None, staging=False):
    target = '/g_business/v1/payments'  
    body = '{ "flow": "MATCH_CODE", "amount_unit": %d, "currency": "%s", "callback_url": "%s"' % (amount_unit, currency, callback_url)
    if external_code:
        body += ', "external_code": "%s"' % external_code
    if metadata:
        body += ', "metadata": %s' % metadata
    if expiration_date:
        body += ', "expiration_date": "%s"' % expiration_date
    body += ' }'
    return send_request(key_id, key, 'post', target, body, idempotency_key, staging)


def get_payment_details(key_id, key, payment_id, staging=False):
    target = '/g_business/v1/payments/%s' % payment_id
    return send_request(key_id, key, 'get', target, '', None, staging)