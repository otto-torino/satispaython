# satispaython

A simple library to manage Satispay payments following the [Web-button flow](https://developers.satispay.com/docs/web-button-pay).

## Requirements

* python >= 3.6
* [`cryptography`](https://github.com/pyca/cryptography) >= 3.1
* [`requests`](https://github.com/psf/requests) >= 2.24

## Installation

You can install this package with pip: `pip install satispaython`.

## Usage

### Key generation

Firs of all you need a RSA private key. You may generate the key by yourself or you may use the provided utility functions:

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

> :information_source: Satispaython key management is based on [`cryptography`](https://cryptography.io/en/latest/) so all the functions which require an RSA key parameter expect an object of the class [`RSAPrivateKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey). If you don't use the `load_key` function then make sure your key is an instance of [`RSAPrivateKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey).

You may protect your key with a password simply adding the `password` parameter:

```python
write_key(rsa_key, 'path/to/file.pem', password='mypassword')
rsa_key = load_key('path/to/file.pem', password='mypassword')
```

### Satispay API

Satispaython web requests are based on [`requests`](https://requests.readthedocs.io/en/master/) so the following functions return an instance of [`Response`](https://requests.readthedocs.io/en/latest/api/#requests.Response). On success, the Satispay API responds with a JSON encoded body, so you can simply check for the [`response.status_code`](https://requests.readthedocs.io/en/latest/api/#requests.Response.status_code) and eventually get the content with [`response.json()`](https://requests.readthedocs.io/en/latest/api/#requests.Response.json).

> :information_source: If you need to use the Sandbox endpoints be sure to read the [section](https://github.com/otto-torino/django-satispaython#sandbox-endpoints).

In order to use the [Satispay API](https://developers.satispay.com/reference) simply import satispaython:

```python
import satispaython as satispay
```

Then you can:

#### Obtain a key-id using a token

```python
response = satispay.obtain_key_id(rsa_key, token)
```

> :information_source: The token is the activation code that can be generated from the Satispay Dashboard (or provided manually for Sandbox account).

> :warning: Tokens are disposable! The key-id should be saved right after its creation.

#### Make an authentication test

```python
response = satispay.test_authentication(key_id, rsa_key)
```

> :information_source: Authentication tests work on [Sandbox](https://developers.satispay.com/docs/sandbox-account) endpoints only.

#### Create a payment

```python
response = satispay.create_payment(key_id, rsa_key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None)
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
response = satispay.get_payment_details(key_id, rsa_key, payment_id)
```

### Sandbox endpoints

By default satispaython uses the production Satispay API. If you need to use the [Sandbox](https://developers.satispay.com/docs/sandbox-account) endpoints, simply set the `staging` parameter to `True`:

```python
response = satispay.obtain_key_id(rsa_key, token, staging=True)
response = satispay.create_payment(key_id, rsa_key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None, staging=True)
response = satispay.get_payment_details(key_id, rsa_key, payment_id, staging=True)
```