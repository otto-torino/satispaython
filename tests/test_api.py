import json
from pathlib import Path

import respx
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from freezegun import freeze_time
from httpx import Headers
from pytest import fixture

import satispaython
from satispaython import AsyncSatispayClient

import pytest


@fixture(scope="module")
def public_key(rsa_key):
    key_encoding = Encoding.PEM
    key_format = PublicFormat.SubjectPublicKeyInfo
    public_pem = rsa_key.public_key().public_bytes(key_encoding, key_format)
    return public_pem.decode()


@fixture(scope="module")
def key_id():
    path = Path(__file__).resolve().parent / "data/key_id.txt"
    with open(path, "r") as file:
        return file.read().strip()


@fixture(scope="module")
def payment_id():
    return "2936affa-ab4c-4daa-9bec-7cafbce4caa1"


@fixture()
def test_authentication_signature():
    path = Path(__file__).resolve().parent / "data/test_authentication_signature.txt"
    with open(path, "r") as file:
        return file.read().strip()


@fixture()
def create_payment_staging_signature():
    path = Path(__file__).resolve().parent / "data/create_payment_staging_signature.txt"
    with open(path, "r") as file:
        return file.read().strip()


@fixture()
def create_payment_production_signature():
    path = (
        Path(__file__).resolve().parent / "data/create_payment_production_signature.txt"
    )
    with open(path, "r") as file:
        return file.read().strip()


@fixture()
def create_payment_staging_no_optionals_signature():
    path = (
        Path(__file__).resolve().parent
        / "data/create_payment_staging_no_optionals_signature.txt"
    )
    with open(path, "r") as file:
        return file.read().strip()


@fixture()
def create_payment_production_no_optionals_signature():
    path = (
        Path(__file__).resolve().parent
        / "data/create_payment_production_no_optionals_signature.txt"
    )
    with open(path, "r") as file:
        return file.read().strip()


@fixture()
def get_payment_details_staging_signature():
    path = (
        Path(__file__).resolve().parent
        / "data/get_payment_details_staging_signature.txt"
    )
    with open(path, "r") as file:
        return file.read().strip()


@fixture()
def get_payment_details_production_signature():
    path = (
        Path(__file__).resolve().parent
        / "data/get_payment_details_production_signature.txt"
    )
    with open(path, "r") as file:
        return file.read().strip()


class TestObtainKeyID:
    @respx.mock
    def test_staging(self, rsa_key, public_key):
        route = respx.post(
            "https://staging.authservices.satispay.com/g_business/v1/authentication_keys"
        )
        satispaython.obtain_key_id("623ECX", rsa_key, True)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content.decode()) == {
            "public_key": public_key,
            "token": "623ECX",
        }
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"

    @respx.mock
    def test_production(self, rsa_key, public_key):
        route = respx.post(
            "https://authservices.satispay.com/g_business/v1/authentication_keys"
        )
        satispaython.obtain_key_id("623ECX", rsa_key)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content.decode()) == {
            "public_key": public_key,
            "token": "623ECX",
        }
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"


class TestTestAuthentication:
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    def test_test_authentication(self, key_id, rsa_key, test_authentication_signature):
        route = respx.post(
            "https://staging.authservices.satispay.com/wally-services/protocol/tests/signature"
        )
        satispaython.test_authentication(key_id, rsa_key)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert request.content is b""
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers["Host"] == "staging.authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{test_authentication_signature}"'
        )


class TestCreatePayment:
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    def test_staging(self, key_id, rsa_key, create_payment_staging_signature):
        route = respx.post(
            "https://staging.authservices.satispay.com/g_business/v1/payments"
        )
        body_params = {
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        headers = Headers({"Idempotency-Key": "test_idempotency_key"})
        satispaython.create_payment(
            key_id, rsa_key, 100, "EUR", body_params, headers, True
        )
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content.decode()) == {
            "flow": "MATCH_CODE",
            "amount_unit": 100,
            "currency": "EUR",
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        assert request.headers["Idempotency-Key"] == "test_idempotency_key"
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers["Host"] == "staging.authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=dOjZtX6Has9wFZQDmriLhIfThHD11nuxFZNIjp7FwR0="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{create_payment_staging_signature}"'
        )

    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    def test_production(self, key_id, rsa_key, create_payment_production_signature):
        route = respx.post("https://authservices.satispay.com/g_business/v1/payments")
        body_params = {
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        headers = Headers({"Idempotency-Key": "test_idempotency_key"})
        satispaython.create_payment(key_id, rsa_key, 100, "EUR", body_params, headers)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content.decode()) == {
            "flow": "MATCH_CODE",
            "amount_unit": 100,
            "currency": "EUR",
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        assert request.headers["Idempotency-Key"] == "test_idempotency_key"
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers["Host"] == "authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=dOjZtX6Has9wFZQDmriLhIfThHD11nuxFZNIjp7FwR0="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{create_payment_production_signature}"'
        )

    @pytest.mark.asyncio
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    async def test_staging_async(
        self, key_id, rsa_key, create_payment_staging_signature
    ):
        route = respx.post(
            "https://staging.authservices.satispay.com/g_business/v1/payments"
        )
        body_params = {
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        headers = {"Idempotency-Key": "test_idempotency_key"}
        async with AsyncSatispayClient(key_id, rsa_key, True) as client:
            await client.create_payment(100, "EUR", body_params, headers)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content.decode()) == {
            "flow": "MATCH_CODE",
            "amount_unit": 100,
            "currency": "EUR",
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        assert request.headers["Idempotency-Key"] == "test_idempotency_key"
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers["Host"] == "staging.authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=dOjZtX6Has9wFZQDmriLhIfThHD11nuxFZNIjp7FwR0="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{create_payment_staging_signature}"'
        )

    @pytest.mark.asyncio
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    async def test_production_async(
        self, key_id, rsa_key, create_payment_production_signature
    ):
        route = respx.post("https://authservices.satispay.com/g_business/v1/payments")
        body_params = {
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        headers = {"Idempotency-Key": "test_idempotency_key"}
        async with AsyncSatispayClient(key_id, rsa_key) as client:
            await client.create_payment(100, "EUR", body_params, headers)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content.decode()) == {
            "flow": "MATCH_CODE",
            "amount_unit": 100,
            "currency": "EUR",
            "callback_url": "https://test.test?payment_id={uuid}",
            "expiration_date": "2019-03-18T16:10:24.000Z",
            "external_code": "test_code",
            "metadata": {"metadata": "test"},
        }
        assert request.headers["Idempotency-Key"] == "test_idempotency_key"
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers["Host"] == "authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=dOjZtX6Has9wFZQDmriLhIfThHD11nuxFZNIjp7FwR0="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{create_payment_production_signature}"'
        )

    class TestWithNoHeadersAndBody:
        @respx.mock
        @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
        def test_staging(
            self, key_id, rsa_key, create_payment_staging_no_optionals_signature
        ):
            route = respx.post(
                "https://staging.authservices.satispay.com/g_business/v1/payments"
            )
            satispaython.create_payment(key_id, rsa_key, 100, "EUR", staging=True)
            assert route.called
            assert route.call_count == 1
            request = route.calls.last.request
            assert request.method == "POST"
            assert json.loads(request.content.decode()) == {
                "flow": "MATCH_CODE",
                "amount_unit": 100,
                "currency": "EUR",
            }
            assert request.headers["Accept"] == "application/json"
            assert request.headers["Content-Type"] == "application/json"
            assert request.headers["Host"] == "staging.authservices.satispay.com"
            assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
            assert (
                request.headers["Digest"]
                == "SHA-256=a5UF/fcWo+KdzPGADk9XDV/CwKsGyrNLNKGind53oVM="
            )
            assert (
                request.headers["Authorization"] == f'Signature keyId="{key_id}", '
                f'algorithm="rsa-sha256", '
                f'headers="(request-target) host date digest", '
                f'signature="{create_payment_staging_no_optionals_signature}"'
            )

        @respx.mock
        @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
        def test_production(
            self, key_id, rsa_key, create_payment_production_no_optionals_signature
        ):
            route = respx.post(
                "https://authservices.satispay.com/g_business/v1/payments"
            )
            satispaython.create_payment(key_id, rsa_key, 100, "EUR")
            assert route.called
            assert route.call_count == 1
            request = route.calls.last.request
            assert request.method == "POST"
            assert json.loads(request.content.decode()) == {
                "flow": "MATCH_CODE",
                "amount_unit": 100,
                "currency": "EUR",
            }
            assert request.headers["Accept"] == "application/json"
            assert request.headers["Content-Type"] == "application/json"
            assert request.headers["Host"] == "authservices.satispay.com"
            assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
            assert (
                request.headers["Digest"]
                == "SHA-256=a5UF/fcWo+KdzPGADk9XDV/CwKsGyrNLNKGind53oVM="
            )
            assert (
                request.headers["Authorization"] == f'Signature keyId="{key_id}", '
                f'algorithm="rsa-sha256", '
                f'headers="(request-target) host date digest", '
                f'signature="{create_payment_production_no_optionals_signature}"'
            )

        @pytest.mark.asyncio
        @respx.mock
        @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
        async def test_staging_async(
            self, key_id, rsa_key, create_payment_staging_no_optionals_signature
        ):
            route = respx.post(
                "https://staging.authservices.satispay.com/g_business/v1/payments"
            )
            async with AsyncSatispayClient(key_id, rsa_key, True) as client:
                await client.create_payment(100, "EUR")
            assert route.called
            assert route.call_count == 1
            request = route.calls.last.request
            assert request.method == "POST"
            assert json.loads(request.content.decode()) == {
                "flow": "MATCH_CODE",
                "amount_unit": 100,
                "currency": "EUR",
            }
            assert request.headers["Accept"] == "application/json"
            assert request.headers["Content-Type"] == "application/json"
            assert request.headers["Host"] == "staging.authservices.satispay.com"
            assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
            assert (
                request.headers["Digest"]
                == "SHA-256=a5UF/fcWo+KdzPGADk9XDV/CwKsGyrNLNKGind53oVM="
            )
            assert (
                request.headers["Authorization"] == f'Signature keyId="{key_id}", '
                f'algorithm="rsa-sha256", '
                f'headers="(request-target) host date digest", '
                f'signature="{create_payment_staging_no_optionals_signature}"'
            )

        @pytest.mark.asyncio
        @respx.mock
        @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
        async def test_production_async(
            self, key_id, rsa_key, create_payment_production_no_optionals_signature
        ):
            route = respx.post(
                "https://authservices.satispay.com/g_business/v1/payments"
            )
            async with AsyncSatispayClient(key_id, rsa_key) as client:
                await client.create_payment(100, "EUR")
            assert route.called
            assert route.call_count == 1
            request = route.calls.last.request
            assert request.method == "POST"
            assert json.loads(request.content.decode()) == {
                "flow": "MATCH_CODE",
                "amount_unit": 100,
                "currency": "EUR",
            }
            assert request.headers["Accept"] == "application/json"
            assert request.headers["Content-Type"] == "application/json"
            assert request.headers["Host"] == "authservices.satispay.com"
            assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
            assert (
                request.headers["Digest"]
                == "SHA-256=a5UF/fcWo+KdzPGADk9XDV/CwKsGyrNLNKGind53oVM="
            )
            assert (
                request.headers["Authorization"] == f'Signature keyId="{key_id}", '
                f'algorithm="rsa-sha256", '
                f'headers="(request-target) host date digest", '
                f'signature="{create_payment_production_no_optionals_signature}"'
            )


class TestGetPaymentDetails:
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    def test_staging(
        self, key_id, rsa_key, payment_id, get_payment_details_staging_signature
    ):
        route = respx.get(
            f"https://staging.authservices.satispay.com/g_business/v1/payments/{payment_id}"
        )
        satispaython.get_payment_details(key_id, rsa_key, payment_id, staging=True)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.content is b""
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Host"] == "staging.authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{get_payment_details_staging_signature}"'
        )

    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    def test_production(
        self, key_id, rsa_key, payment_id, get_payment_details_production_signature
    ):
        route = respx.get(
            f"https://authservices.satispay.com/g_business/v1/payments/{payment_id}"
        )
        satispaython.get_payment_details(key_id, rsa_key, payment_id)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.content is b""
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Host"] == "authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{get_payment_details_production_signature}"'
        )

    @pytest.mark.asyncio
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    async def test_staging_async(
        self, key_id, rsa_key, payment_id, get_payment_details_staging_signature
    ):
        route = respx.get(
            f"https://staging.authservices.satispay.com/g_business/v1/payments/{payment_id}"
        )
        async with AsyncSatispayClient(key_id, rsa_key, True) as client:
            await client.get_payment_details(payment_id)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.content is b""
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Host"] == "staging.authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{get_payment_details_staging_signature}"'
        )

    @pytest.mark.asyncio
    @respx.mock
    @freeze_time("Mon, 18 Mar 2019 15:10:24 +0000")
    async def test_production_async(
        self, key_id, rsa_key, payment_id, get_payment_details_production_signature
    ):
        route = respx.get(
            f"https://authservices.satispay.com/g_business/v1/payments/{payment_id}"
        )
        async with AsyncSatispayClient(key_id, rsa_key) as client:
            await client.get_payment_details(payment_id)
        assert route.called
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.content is b""
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Host"] == "authservices.satispay.com"
        assert request.headers["Date"] == "Mon, 18 Mar 2019 15:10:24 +0000"
        assert (
            request.headers["Digest"]
            == "SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="
        )
        assert (
            request.headers["Authorization"] == f'Signature keyId="{key_id}", '
            f'algorithm="rsa-sha256", '
            f'headers="(request-target) host date digest", '
            f'signature="{get_payment_details_production_signature}"'
        )
