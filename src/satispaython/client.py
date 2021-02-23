from typing import Optional, Tuple

from httpx import Client, AsyncClient, Headers, URL, Response
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from .auth import SatispayAuth


class SatispayClientMixin:

    @staticmethod
    def _initialize(
        key_id: str,
        rsa_key: RSAPrivateKey,
        headers: Headers,
        staging: bool,
    ) -> Tuple[SatispayAuth, Headers, URL]:
        auth = SatispayAuth(key_id, rsa_key)
        headers.update({'Accept': 'application/json'})
        if staging:
            base_url = URL('https://staging.authservices.satispay.com')
        else:
            base_url = URL('https://authservices.satispay.com')
        return auth, headers, base_url

    @staticmethod
    def _prepare_create_payment(
        amount_unit: int,
        currency: str,
        body_params: dict,
        headers: Headers
    ) -> Tuple[URL, dict, Headers]:
        target = URL('/g_business/v1/payments')
        headers.update({'Content-Type': 'application/json'})
        body_params.update({'flow': 'MATCH_CODE', 'amount_unit': amount_unit, 'currency': currency})
        return target, body_params, headers

    @staticmethod
    def _prepare_get_payment_details(payment_id: str) -> URL:
        return URL(f'/g_business/v1/payments/{payment_id}')


class SatispayClient(Client, SatispayClientMixin):

    def __init__(self, key_id: str, rsa_key: RSAPrivateKey, staging: bool = False, **kwargs) -> None:
        headers = kwargs.get('headers', Headers())
        auth, headers, base_url = self._initialize(key_id, rsa_key, headers, staging)
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    def create_payment(
        self,
        amount_unit: int,
        currency: str,
        body_params: Optional[dict] = None,
        headers: Optional[Headers] = None
    ) -> Response:
        body_params, headers = body_params or {}, headers or Headers()
        target, body, headers = self._prepare_create_payment(amount_unit, currency, body_params, headers)
        return self.post(target, json=body, headers=headers)

    def get_payment_details(self, payment_id: str, headers: Optional[Headers] = None) -> Response:
        target = self._prepare_get_payment_details(payment_id)
        return self.get(target, headers=headers)


class AsyncSatispayClient(AsyncClient, SatispayClientMixin):

    def __init__(self, key_id: str, rsa_key: RSAPrivateKey, staging: bool = False, **kwargs) -> None:
        headers = kwargs.get('headers', Headers())
        auth, headers, base_url = self._initialize(key_id, rsa_key, headers, staging)
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    async def create_payment(
        self,
        amount_unit: int,
        currency: str,
        body_params: Optional[dict] = None,
        headers: Optional[Headers] = None
    ) -> Response:
        body_params, headers = body_params or {}, headers or Headers()
        target, body, headers = self._prepare_create_payment(amount_unit, currency, body_params, headers)
        return await self.post(target, json=body, headers=headers)

    async def get_payment_details(self, payment_id: str, headers: Optional[Headers] = None) -> Response:
        target = self._prepare_get_payment_details(payment_id)
        return await self.get(target, headers=headers)
