# satispaython

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/otto-torino/satispaython/Test?style=flat-square)](https://github.com/otto-torino/satispaython/actions)
[![Codecov](https://img.shields.io/codecov/c/github/otto-torino/satispaython?style=flat-square)](https://codecov.io/gh/otto-torino/satispaython)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/satispaython?style=flat-square)](https://pypi.org/project/satispaython)

A simple library to manage Satispay payments following the [Web-button flow](https://developers.satispay.com/docs/web-button-pay).

## Requirements

* [`cryptography`](https://github.com/pyca/cryptography) >= 3.3
* [`httpx`](https://github.com/encode/httpx) >= 0.16

## Installation

You can install this package with pip: `pip install satispaython`.

## Usage

### Key generation

First of all you need a RSA private key. You may generate the key by yourself or you may use the provided utility functions:

```python
from satispaython.utils import generate_key, write_key

rsa_key = generate_key()
write_key(rsa_key, 'path/to/file.pem')
```

In order to load the key from a PEM encoded file you may use the utility function:

```python
from satispaython.utils import load_key

rsa_key = load_key('path/to/file.pem')
```

> :information_source: The function `write_key` stores the key in the PEM format. If you generate the key with any other method and you would like to use the `load_key` function, please make sure the key is stored within a file in the PEM format.

> :information_source: Satispaython key management is based on `cryptography` so all the functions which require an RSA key parameter expect an object of the class [`RSAPrivateKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa.html#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey). If you don't use the `load_key` function then make sure your key is an instance of `RSAPrivateKey`.

You may protect your key with a password simply adding the `password` parameter:

```python
write_key(rsa_key, 'path/to/file.pem', password='mypassword')
rsa_key = load_key('path/to/file.pem', password='mypassword')
```

### Satispay API

Satispaython web requests are based on `httpx` so the following functions return an instance of [`Response`](https://www.python-httpx.org/api/#response). On success, the Satispay API responds with a JSON encoded body, so you can simply check for the `response.status_code` and eventually get the content with `response.json()`.

> :information_source: If you need to use the Sandbox endpoints be sure to read the [proper section](https://github.com/otto-torino/satispaython#sandbox-endpoints).

In order to use the [Satispay API](https://developers.satispay.com/reference) simply import satispaython:

```python
import satispaython
```

Then you can:

#### Obtain a key-id using a token

```python
response = satispaython.obtain_key_id(token, rsa_key)
```

> :information_source: The token is the activation code that can be generated from the Satispay Dashboard (or provided manually for Sandbox account).

> :warning: Tokens are disposable! The key-id should be saved right after its creation.

#### Make an authentication test

```python
response = satispaython.test_authentication(key_id, rsa_key)
```

> :information_source: Authentication tests work on Sandbox endpoints only.

#### Create a payment

```python
response = satispaython.create_payment(key_id, rsa_key, amount_unit, currency, body_params=None, headers=None)
```

You may use the utility function `format_datetime` to get a correctly formatted `expiration_date` to supply to the request:

```python
from datetime import datetime, timezone, timedelta
from satispaython.utils import format_datetime

expiration_date = datetime.now(timezone.utc) + timedelta(hours=1)
expiration_date = format_datetime(expiration_date)
```

#### Get payment details

```python
response = satispaythonsatispaython.get_payment_details(key_id, rsa_key, payment_id, headers=None)
```

### Sandbox endpoints

By default satispaython points to the production Satispay API. If you need to use the [Sandbox](https://developers.satispay.com/docs/sandbox-account) endpoints, simply set the `staging` parameter to `True`:

```python
response = satispaython.obtain_key_id(rsa_key, token, staging=True)
response = satispaython.create_payment(key_id, rsa_key, amount_unit, currency, body_params=None, headers=None, staging=True)
response = satispaython.get_payment_details(key_id, rsa_key, payment_id, headers=None, staging=True)
```

## Clients, AsyncClients and Auth

Satispaython offers specialized versions of `httpx`'s [`Client`](https://www.python-httpx.org/api/#client), [`AsyncClient`](https://www.python-httpx.org/api/#asyncclient) and [`Auth`](https://www.python-httpx.org/advanced/#customizing-authentication) classes:

```python
from satispaython import SatispayClient

with SatispayClient(key_id, rsa_key, staging=True) as client:
    response = client.create_payment(100, 'EUR', body_params=None, headers=None)
    response = client.get_payment_details(payment_id, headers=None)
```

```python
from satispaython import AsyncSatispayClient

async with AsyncSatispayClient(key_id, rsa_key, staging=True) as client:
    response = await client.create_payment(100, 'EUR', body_params=None, headers=None)
    response = await client.get_payment_details(payment_id, headers=None)
```

```python
import httpx
from satispaython import SatispayAuth

auth = SatispayAuth(key_id, rsa_key)
response = httpx.post('https://staging.authservices.satispay.com/wally-services/protocol/tests/signature', auth=auth)
```
