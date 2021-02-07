from httpx import Client

from ._auth import SatispayAuth


class SatispayClient(Client):

    def __init__(self, key_id, rsa_key, staging=False, **kwargs):
        auth = SatispayAuth(key_id, rsa_key)
        headers = kwargs.get('headers', {})
        headers.update({'Accept': 'application/json'})
        base_url = 'https://staging.authservices.satispay.com' if staging else 'https://authservices.satispay.com'
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    def test_authentication(self):
        target = '/wally-services/protocol/tests/signature'
        headers = {'Content-Type': 'application/json'}
        return self.post(target, headers=headers)

    def create_payment(self, amount_unit, currency, body_params=None, headers=None):
        target = '/g_business/v1/payments'
        headers = headers or {}
        headers.update({'Content-Type': 'application/json'})
        body = {'flow': 'MATCH_CODE', 'amount_unit': amount_unit, 'currency': currency}
        body.update(body_params or {})
        return self.post(target, json=body, headers=headers)

    def get_payment_details(self, payment_id, headers=None):
        target = f'/g_business/v1/payments/{payment_id}'
        return self.get(target, headers=headers)
