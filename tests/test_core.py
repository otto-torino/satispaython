from pytest import fixture, mark
from datetime import datetime
from satispaython._core import *


# @fixture
# def idempotency_key():
#     return 'test_idempotency_key'

# @fixture
# def common_headers():
#     return { 'Accept': 'application/json' }

# @fixture
# def post_put_headers():
#     return { 'Content-Type': 'application/json' }

# @fixture
# def authorization_headers(host, date, digest, authorization_header):
#     return { 'Host': host, 'Date': date, 'Digest': digest, 'Authorization': authorization_header }

# @fixture
# def idempotency_key_headers(idempotency_key):
#     return { 'Idempotency-Key': idempotency_key }

# @fixture
# def obtain_key_id_body():
#     return f'{{ "public_key": {key}, "token": "623ECX" }}'

@fixture
def body():
    return '{\n  "flow": "MATCH_CODE",\n  "amount_unit": 100,\n  "currency": "EUR"\n}'

@fixture
def digest():
    return 'SHA-256=ZML76UQPYzw5yDTmhySnU1S8nmqGde/jhqOG5rpfVSI='

@fixture
def target():
    return '/wally-services/protocol/tests/signature'

@fixture
def host():
    return 'staging.authservices.satispay.com'

@fixture
def date():
    return 'Mon, 18 Mar 2019 15:10:24 +0000'

@fixture
def string(target, host, date, digest):
    return f'(request-target): post {target}\nhost: {host}\ndate: {date}\ndigest: {digest}'

@fixture
def signature():
    return 'q3m7sSNNeWbYDVfhMhK9/y7iLMdvxJMxHkVlMW9A51k50w3Ci2o7bp96Y08oVbFIJa3E0sfSbvJuI9CYvcv8bNyhVy7remL5mx21TN2VgZJlHlrE8UMBD6BbWKWjRJi9RwntNMHLUmlSkKSYzChFRI2V1wfN1JFrfXEfCQ6q3TjRnBynfO6SLJg16nHXeRJPqMhO/nVJOvdhMQgGlDoG2W11q5LJuvzKbH0CoKCaKNXRHbUsnR381aH+lf/4rKBPNSHP2Vk5yJve9DC9sTU09MT/c37rfXKuF2o07TZnDH/3Fxws4Wl+9WybXRX1CWUmTuFf3zmwRG5LlK5Gr4dRuE6NPXWHZ+tOe3zSA79/NA1mFxbVzlezOCXTy7z4RB1woMlXs6S/zgZ0ATDaFi8X5DqA6++bgUIDkkczKJLq9Fa7iUeVHvnIsYKp9uHwnA0bmlYCQiUHrju51auGdoonRkpwzHNYA22EqtRlJLn0Bt0gJJz2XkKwufob4YeOv8N3K3mdrZ2C1YoYn2ARidM4iVqLp7zAM81GW7lESeMipCJXfv5dbRAcG7jMyZPiZ6hWjGJ10/Wbx/z5QBX2HQxpl/vyXyUBTPBnpnmBco2VEv09OeYi1IR+2OCkF7OPbqvKww8JxHvW8OpX2/tExaG1y3P9mRDYTWbeemjwUs6CUzw='

@fixture
def key_id():
    return '4ekqhmf77q95deciis2frre12el393rteletbrg4rffqri3n58lsjsvf6uph934o7vr69r93iu4ifc3tkeidlg5fhoogo3grmh99lr2g94a6aerbf56m48og47e6vnbfu13rf1vvj3l4b3mn3qd2ttoc4a8hh2jgb589s59d56tdmp7dkuobesvfmnnpf8cmg7646do5'

@fixture
def authorization_header(key_id, signature):
    return f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="{signature}"'

@fixture
def authorization_headers(host, date, digest, authorization_header):
    return { 'Host': host, 'Date': date, 'Digest': digest, 'Authorization': authorization_header }


def test_get_formatted_date():
    date = get_formatted_date()
    assert datetime.strptime(date, '%a, %d %b %Y %H:%M:%S +0000')

def test_compute_digest(body, digest):
    assert compute_digest(body) == digest

def test_generate_string(target, host, date, digest, string):
    assert generate_string('post', target, host, date, digest) == string

def test_sign_string(key, string, signature):
    assert sign_string(key, string) == signature

def test_compute_authorization_header(key_id, signature, authorization_header):
    assert compute_authorization_header(key_id, signature) == authorization_header

def test_compute_authorization_headers(key_id, key, target, host, body, authorization_headers, mock_date):
    assert compute_authorization_headers(key_id, key, 'post', target, host, body) == authorization_headers


# class TestGenerateHeaders:

#     def test_obtain_key_id_headers(self, target, host, obtain_key_id_body, common_headers, post_put_headers):
#         headers = common_headers | post_put_headers
#         assert generate_headers(None,   None, 'post',  target, host, obtain_key_id_body, None) == headers

#     def test_authentication_headers(self, key_id, key, target, host, payment_body, common_headers, post_put_headers, authorization_headers):
#         headers = common_headers | post_put_headers | authorization_headers
#         assert generate_headers(key_id, key,  'post',  target, host, payment_body, None) == headers

#     def test_get_payment_details_headers(self, key_id, key, target, host, common_headers, authorization_headers):
#         headers = common_headers | post_put_headers | authorization_headers
#         assert generate_headers(key_id, key,  'get',   target, host, None, None) == headers

#     class TestGeneratePaymentHeaders:

#         def test_without_idempotency_key(self, key_id, key, target, host, payment_body, common_headers, post_put_headers, authorization_headers):
#             headers = common_headers | post_put_headers | authorization_headers
#             assert generate_headers(key_id, key,  'post',  target, host, payment_body, None) == headers

#         def test_with_idempotency_key(self, key_id, key, target, host, payment_body, common_headers, post_put_headers, authorization_headers):
#             headers = common_headers | post_put_headers | authorization_headers | idempotency_key_headers
#             assert generate_headers(key_id, key,  'post',  target, host, payment_body, idempotency_key) == headers
