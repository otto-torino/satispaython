from base64 import b64encode
from datetime import datetime, timezone
from hashlib import sha256
from typing import Generator

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from httpx import Auth, Request, Headers, Response


class SatispayAuth(Auth):
    requires_request_body = True

    def __init__(self, key_id: str, rsa_key: RSAPrivateKey) -> None:
        self._key_id = key_id
        self._rsa_key = rsa_key

    @staticmethod
    def _get_formatted_date() -> str:
        date = datetime.now(timezone.utc)
        return date.strftime('%a, %d %b %Y %H:%M:%S %z')

    @staticmethod
    def _compute_digest(request: Request) -> str:
        digest = sha256(request.content).digest()
        digest = b64encode(digest).decode()
        return f'SHA-256={digest}'

    @staticmethod
    def _compose_string(request: Request, date: str, digest: str) -> str:
        method, target, host = request.method, request.url.path, request.url.host
        return f'(request-target): {method.lower()} {target}\nhost: {host}\ndate: {date}\ndigest: {digest}'

    def _sign_string(self, string: str) -> str:
        signature = self._rsa_key.sign(string.encode(), PKCS1v15(), SHA256())
        return b64encode(signature).decode()

    def _compose_authorization_header(self, signature: str) -> str:
        return f'Signature keyId="{self._key_id}", ' \
               f'algorithm="rsa-sha256", ' \
               f'headers="(request-target) host date digest", ' \
               f'signature="{signature}"'

    def _generate_authorization_headers(self, request: Request) -> Headers:
        date = self._get_formatted_date()
        digest = self._compute_digest(request)
        string = self._compose_string(request, date, digest)
        signature = self._sign_string(string)
        authorization_header = self._compose_authorization_header(signature)
        headers = {'Host': request.url.host, 'Date': date, 'Digest': digest, 'Authorization': authorization_header}
        return Headers(headers)

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        authorization_headers = self._generate_authorization_headers(request)
        request.headers.update(authorization_headers)
        yield request
