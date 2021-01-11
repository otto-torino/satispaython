import json

from base64 import b64encode
from hashlib import sha256
from datetime import datetime, timezone

import requests

from cryptography.hazmat.primitives.asymmetric import padding as paddings
from cryptography.hazmat.primitives import hashes


def get_formatted_date():
    return datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %z')


def compute_digest(body):
    body = body.encode()
    digest = b64encode(sha256(body).digest())
    digest = digest.decode()
    return f'SHA-256={digest}'


def generate_string(method, target, host, date, digest):
    return f'(request-target): {method} {target}\nhost: {host}\ndate: {date}\ndigest: {digest}'


def sign_string(key, string):
    string = string.encode()
    signature = key.sign(data=string, padding=paddings.PKCS1v15(), algorithm=hashes.SHA256())
    return b64encode(signature).decode()


def compute_authorization_header(key_id, signature):
    return f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="{signature}"'


def compute_authorization_headers(key_id, key, method, target, host, body):
    date = get_formatted_date()
    digest = compute_digest(body)
    string = generate_string(method, target, host, date, digest)
    signature = sign_string(key, string)
    authorization_header = compute_authorization_header(key_id, signature)
    return {'Host': host, 'Date': date, 'Digest': digest, 'Authorization': authorization_header}


def generate_headers(key_id, key, method, target, host, body, idempotency_key):
    headers = {'Accept': 'application/json'}
    if method in ('post', 'put'):
        headers.update({'Content-Type': 'application/json'})
    if idempotency_key:
        headers.update({'Idempotency-Key': idempotency_key})
    if key_id and key:
        headers.update(compute_authorization_headers(key_id, key, method, target, host, body))
    return headers


def send_request(key_id, key, method, target, body, idempotency_key, staging):
    host = 'staging.authservices.satispay.com' if staging else 'authservices.satispay.com'
    body = json.dumps(body) if body else ''
    headers = generate_headers(key_id, key, method, target, host, body, idempotency_key)
    url = f'https://{host}{target}'
    return getattr(requests, method)(url=url, data=body, headers=headers)
