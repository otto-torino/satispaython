from typing import Optional

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from httpx import URL, AsyncClient, Client, Headers, Response

from .auth import SatispayAuth


class SatispayClient(Client):
    def __init__(
        self, key_id: str, rsa_key: RSAPrivateKey, staging: bool = False, **kwargs
    ) -> None:
        auth = SatispayAuth(key_id, rsa_key)
        headers = kwargs.get("headers", Headers())
        headers.update({"Accept": "application/json"})
        if staging:
            base_url = URL("https://staging.authservices.satispay.com")
        else:
            base_url = URL("https://authservices.satispay.com")
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    def create_payment(
        self,
        amount_unit: int,
        currency: str,
        body_params: Optional[dict] = None,
        headers: Optional[Headers] = None,
    ) -> Response:
        target = URL("/g_business/v1/payments")
        try:
            headers.update({"Content-Type": "application/json"})
        except AttributeError:
            headers = Headers({"Content-Type": "application/json"})
        try:
            body_params.update(
                {"flow": "MATCH_CODE", "amount_unit": amount_unit, "currency": currency}
            )
        except AttributeError:
            body_params = {
                "flow": "MATCH_CODE",
                "amount_unit": amount_unit,
                "currency": currency,
            }
        return self.post(target, json=body_params, headers=headers)

    def get_payment_details(
        self, payment_id: str, headers: Optional[Headers] = None
    ) -> Response:
        target = URL(f"/g_business/v1/payments/{payment_id}")
        return self.get(target, headers=headers)


class AsyncSatispayClient(AsyncClient):
    def __init__(
        self, key_id: str, rsa_key: RSAPrivateKey, staging: bool = False, **kwargs
    ) -> None:
        auth = SatispayAuth(key_id, rsa_key)
        headers = kwargs.get("headers", Headers())
        headers.update({"Accept": "application/json"})
        if staging:
            base_url = URL("https://staging.authservices.satispay.com")
        else:
            base_url = URL("https://authservices.satispay.com")
        super().__init__(auth=auth, headers=headers, base_url=base_url, **kwargs)

    async def create_payment(
        self,
        amount_unit: int,
        currency: str,
        body_params: Optional[dict] = None,
        headers: Optional[Headers] = None,
    ) -> Response:
        target = URL("/g_business/v1/payments")
        try:
            headers.update({"Content-Type": "application/json"})
        except AttributeError:
            headers = Headers({"Content-Type": "application/json"})
        try:
            body_params.update(
                {"flow": "MATCH_CODE", "amount_unit": amount_unit, "currency": currency}
            )
        except AttributeError:
            body_params = {
                "flow": "MATCH_CODE",
                "amount_unit": amount_unit,
                "currency": currency,
            }
        return await self.post(target, json=body_params, headers=headers)

    async def get_payment_details(
        self, payment_id: str, headers: Optional[Headers] = None
    ) -> Response:
        target = URL(f"/g_business/v1/payments/{payment_id}")
        return await self.get(target, headers=headers)
