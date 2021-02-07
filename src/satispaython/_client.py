from httpx import Client, AsyncClient

from ._auth import SatispayAuth


class SatispayClientMixin:

    @staticmethod
    def _initialize(key_id, rsa_key, staging, kwargs):
        auth = SatispayAuth(key_id, rsa_key)
        headers = kwargs.get('headers', {})
        headers.update({'Accept': 'application/json'})
        base_url = 'https://staging.authservices.satispay.com' if staging else 'https://authservices.satispay.com'
        return auth, headers, base_url

    @staticmethod
    def _prepare_create_payment(amount_unit, currency, body_params, headers):
        target = '/g_business/v1/payments'
        headers = headers or {}
        headers.update({'Content-Type': 'application/json'})
        body = {'flow': 'MATCH_CODE', 'amount_unit': amount_unit, 'currency': currency}
        body.update(body_params or {})
        return target, body, headers

    @staticmethod
    def _prepare_get_payment_details(payment_id):
        return f'/g_business/v1/payments/{payment_id}'


class SatispayClient(Client, SatispayClientMixin):

    def __init__(self, key_id, rsa_key, staging=False, **kwargs):
        auth, headers, base_url = self._initialize(key_id, rsa_key, staging, kwargs)
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    def create_payment(self, amount_unit, currency, body_params=None, headers=None):
        target, body, headers = self._prepare_create_payment(amount_unit, currency, body_params, headers)
        return self.post(target, json=body, headers=headers)

    def get_payment_details(self, payment_id, headers=None):
        target = self._prepare_get_payment_details(payment_id)
        return self.get(target, headers=headers)


class AsyncSatispayClient(AsyncClient, SatispayClientMixin):

    def __init__(self, key_id, rsa_key, staging=False, **kwargs):
        auth, headers, base_url = self._initialize(key_id, rsa_key, staging, kwargs)
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    async def create_payment(self, amount_unit, currency, body_params=None, headers=None):
        target, body, headers = self._prepare_create_payment(amount_unit, currency, body_params, headers)
        return await self.post(target, json=body, headers=headers)

    async def get_payment_details(self, payment_id, headers=None):
        target = self._prepare_get_payment_details(payment_id)
        return await self.get(target, headers=headers)
