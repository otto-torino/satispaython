import requests, json

from satispaython.exceptions import UnexpectedRequestMethod
from base64 import b64encode
from hashlib import sha256
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import padding as paddings
from cryptography.hazmat.primitives import hashes


def get_formatted_date():
    return datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %z')


def compute_digest(body):
    body = body.encode('utf-8')
    digest = b64encode(sha256(body).digest())
    digest = digest.decode('utf-8')
    return f'SHA-256={digest}' 


def generate_string(method, target, host, date, digest):
    return f'(request-target): {method} {target}\nhost: {host}\ndate: {date}\ndigest: {digest}'


def sign_string(key, string):
    string = string.encode('utf-8')
    padding = paddings.PSS(mgf=paddings.MGF1(hashes.SHA256()), salt_length=paddings.PSS.MAX_LENGTH)
    signature = key.sign(data=string, padding=paddings.PKCS1v15(), algorithm=hashes.SHA256())
    return b64encode(signature).decode('utf-8')


def compute_authorization_header(key_id, signature):
    return f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="{signature}"'
    

def compute_authorization_headers(key, key_id, method, target, host, body):
    date = get_formatted_date()
    digest = compute_digest(body)
    string = generate_string(method, target, host, date, digest)
    signature = sign_string(key, string)
    header = compute_authorization_header(key_id, signature)
    return { 'Host': host, 'Date': date, 'Digest': digest, 'Authorization': header }


def generate_headers(key, key_id, method, target, host, body, idempotency_key):
    headers = { 'Accept': 'application/json' }
    if method == 'post' or method == 'put':
        headers = { **headers, 'Content-Type': 'application/json' }
    if idempotency_key:
        headers = { **headers, 'Idempotency-Key': idempotency_key }
    if key and key_id:
        authorization_headers = compute_authorization_headers(key, key_id, method, target, host, body)
        headers = { **headers, **authorization_headers }
    return headers


def send_request(key_id, key, method, target, body, idempotency_key, staging):
    host = 'staging.authservices.satispay.com' if staging == True else 'authservices.satispay.com'
    body = json.dumps(body) if body else ''
    headers = generate_headers(key, key_id, method, target, host, body, idempotency_key)
    url = f'https://{host}{target}'
    if method == 'get':
        return requests.get(url=url, data=body, headers=headers)
    elif method == 'post':
        return requests.post(url=url, data=body, headers=headers)
    else:
        raise exceptions.UnexpectedRequestMethod('The request method is invalid (should be "get" or "post")')
