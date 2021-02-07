from base64 import b64encode
from datetime import datetime, timezone
from hashlib import sha256

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as paddings
from httpx import Auth


class SatispayAuth(Auth):
    requires_request_body = True

    def __init__(self, key_id, rsa_key):
        self._key_id = key_id
        self._rsa_key = rsa_key

    @staticmethod
    def _get_formatted_date():
        date = datetime.now(timezone.utc)
        return date.strftime('%a, %d %b %Y %H:%M:%S %z')

    @staticmethod
    def _compute_digest(request):
        digest = sha256(request.content).digest()
        digest = b64encode(digest).decode()
        return f'SHA-256={digest}'

    @staticmethod
    def _compose_string(request, date, digest):
        method, target, host = request.method, request.url.path, request.url.host
        return f'(request-target): {method.lower()} {target}\nhost: {host}\ndate: {date}\ndigest: {digest}'

    def _sign_string(self, string):
        signature = self._rsa_key.sign(string.encode(), paddings.PKCS1v15(), hashes.SHA256())
        return b64encode(signature).decode()

    def _compose_authorization_header(self, signature):
        return f'Signature keyId="{self._key_id}", ' \
               f'algorithm="rsa-sha256", ' \
               f'headers="(request-target) host date digest", ' \
               f'signature="{signature}"'

    def _generate_authorization_headers(self, request):
        date = self._get_formatted_date()
        digest = self._compute_digest(request)
        string = self._compose_string(request, date, digest)
        signature = self._sign_string(string)
        authorization_header = self._compose_authorization_header(signature)
        return {'Host': request.url.host, 'Date': date, 'Digest': digest, 'Authorization': authorization_header}

    def auth_flow(self, request):
        authorization_headers = self._generate_authorization_headers(request)
        request.headers.update(authorization_headers)
        yield request
