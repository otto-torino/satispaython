import responses, json, satispaython

from freezegun import freeze_time
from cryptography.hazmat.primitives import serialization
from pytest import fixture


@fixture(scope='module')
def public_key(key):
    public_pem = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return public_pem.decode()

@fixture(scope='module')
def key_id():
    return '4ekqhmf77q95deciis2frre12el393rteletbrg4rffqri3n58lsjsvf6uph934o7vr69r93iu4ifc3tkeidlg5fhoogo3grmh99lr2g94a6aerbf56m48og47e6vnbfu13rf1vvj3l4b3mn3qd2ttoc4a8hh2jgb589s59d56tdmp7dkuobesvfmnnpf8cmg7646do5'

@fixture(scope='module')
def payment_id():
    return '2936affa-ab4c-4daa-9bec-7cafbce4caa1'


class TestObtainKeyID:

    @responses.activate
    def test_staging(self, key, public_key):
        responses.add(responses.POST, 'https://authservices.satispay.com/g_business/v1/authentication_keys', body='{}', status=200)
        response = satispaython.obtain_key_id(key, '623ECX')
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'POST'
        assert json.loads(request.body) == { 'public_key': public_key , 'token': '623ECX' }
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }.items()

    @responses.activate 
    def test_production(self, key, public_key):
        responses.add(responses.POST, 'https://staging.authservices.satispay.com/g_business/v1/authentication_keys', body='{}', status=200)
        response = satispaython.obtain_key_id(key, '623ECX', True)
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'POST'
        assert json.loads(request.body) == { 'public_key': public_key , 'token': '623ECX' }
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }.items()

class TestAuthentication:

    @responses.activate
    @freeze_time('Mon, 18 Mar 2019 15:10:24 +0000')
    def test_authentication(self, key_id, key):
        responses.add(responses.POST, 'https://staging.authservices.satispay.com/wally-services/protocol/tests/signature', body='{}', status=200)
        response = satispaython.test_authentication(key_id, key)
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'POST'
        assert request.body == None
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Host': 'staging.authservices.satispay.com',
            'Date': 'Mon, 18 Mar 2019 15:10:24 +0000',
            'Digest': 'SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=',
            'Authorization': f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="CIVlKFhdkGinRsaawmk2qM4I8YwMcwdYk2yL/NkLyStufkHmW6EbhAsht7OmHwgcK5wYpl8HhdDAWCFsxTVTSlc84cFLMiMo21Km0YsMM4BObVsxrLshyZ+8Aj4h64JJMRth8m5U2WZA+fnXcvUMAJzOYivPvmWN2fj4cLVtLbrnG0UirND6z3XYIJwJmcwEzChHyaGYeEJrqcvQ8bhyfS9GzlK5XynpiUwpPg7OAePXDIdPVXiK7vXTOrKRXRjrw2sFOoHlLSyOJL91nhQqUBbclpK4XH7n1hAoMbjIur9MvGF9ls48wyiR0ImJHD1JC+wn4mYEYtlrNxnnTKuJiUBGod31N/y6wN6Fy8usiqJ7CX/koPkZdw+bfZx8+gEGF8YMikDXaKmYy2kDJJ6D8aQgPBk5z2ymkrWQXMQwoNMY23IMVxCeCLRbQtQIXfS5zzA47FLDZINHfkgmlRE4XmIABCQte4fWyIm0qk+k5Rckvw1PaeEzIz3s8+O2b0f6PayQ0WrdVIBeVod2TnyHXpT54Xg2sDrVUT6spiL8SBbCZ0diO4+xvBEGUm5yhLVUyNCpwEM1nmsLREhazEd7xNl7e8jPZGiXAAv8g5lI9BLcgq+D6z/uSlXkjTP8Dol/mkcKSAeYr66eZ18q2JyQ6LsSthW3s4rb+DltZdpNwiw="'
        }.items()

class TestCreatePaymet:

    @responses.activate
    @freeze_time('Mon, 18 Mar 2019 15:10:24 +0000')
    def test_staging(self, key_id, key):
        responses.add(responses.POST, 'https://staging.authservices.satispay.com/g_business/v1/payments', body='{}', status=200)
        response = satispaython.create_payment(key_id, key, 100, 'EUR', 'https://test.test?payment_id={uuid}', '2019-03-18T16:10:24.000Z', 'test_code', {'metadata': 'test'}, 'test_idempotency_key', True)
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'POST'
        assert json.loads(request.body) == {
            'flow': 'MATCH_CODE',
            'amount_unit': 100,
            'currency': 'EUR',
            'callback_url': 'https://test.test?payment_id={uuid}',
            'expiration_date': '2019-03-18T16:10:24.000Z',
            'external_code': 'test_code',
            'metadata': { 'metadata': 'test' }
        }
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Idempotency-Key': 'test_idempotency_key',
            'Host': 'staging.authservices.satispay.com',
            'Date': 'Mon, 18 Mar 2019 15:10:24 +0000',
            'Digest': 'SHA-256=gx/Ygi6/J4wFiNAWmbfiE4hZBN/rndG1On+OXyKAaSQ=',
            'Authorization': f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="OtKu4NW77DeHvcIwLIVZHMuGXevdW4SINDYfeZfl+xvfVXx305mbl7Ly8vd7SqgoZDRoq+Z3x0jHGytjzmSxUTbJ2A/OKirFb7AP70V4OnvNHHBBFIrxCLh/dm6Q96Qf67P5uM2/SEVLRWV9AOUwrHiJ3OpiOu975dACCt6wahr/FVTN4W5hbmlI+tOVI8S1SjoL/BIK+1hAIKrUSMWcCvMfISx7/S9m7O9gV7fok973EFTqv/Vd7dF3zCSmWMHGRXkIytB5qQWuKvGGiQI1rNAI/d2xOUxk2+/Zm7hodMEJxfndo0jL4+zQ2wMven+BoPF6CWx24q/O5IuP6CDglQLzr2S26vpQfHNjph8v7xTiLW3LCYVKrHvbT1Z/ovyRKQPmjZTMZz+67AIcC8RJXD0we4+WhQdEgzTcW06ur/HlkoJZUEtqoA5CxrkO0XBLuWTusUdZtK+Edz7AyY7RSsjgHgr57BKIraLBUI2ZbU9nJcjWwDaNWZ57mcO5M4TIJRQVszgYG87/f9QJB738aiqfhNQh+OjX6d9e2RlJseXmc0yIk4waqCwsMDFLtj0uFmb5YdHrdzaDglMicXzKc0bD1YVDa5t7dzTXoTPx5xEO4pYx3tIKsDQ+FJ+C5aqamkR+bLg4F7XUuliGbOaR6Rihwyoxu5wqotbvJ0e8xUY="'
        }.items()

    @responses.activate
    @freeze_time('Mon, 18 Mar 2019 15:10:24 +0000')
    def test_production(self, key_id, key):
        responses.add(responses.POST, 'https://authservices.satispay.com/g_business/v1/payments', body='{}', status=200)
        response = satispaython.create_payment(key_id, key, 100, 'EUR', 'https://test.test?payment_id={uuid}', '2019-03-18T16:10:24.000Z', 'test_code', {'metadata': 'test'}, 'test_idempotency_key')
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'POST'
        assert json.loads(request.body) == {
            'flow': 'MATCH_CODE',
            'amount_unit': 100,
            'currency': 'EUR',
            'callback_url': 'https://test.test?payment_id={uuid}',
            'expiration_date': '2019-03-18T16:10:24.000Z',
            'external_code': 'test_code',
            'metadata': { 'metadata': 'test' }
        }
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Idempotency-Key': 'test_idempotency_key',
            'Host': 'authservices.satispay.com',
            'Date': 'Mon, 18 Mar 2019 15:10:24 +0000',
            'Digest': 'SHA-256=gx/Ygi6/J4wFiNAWmbfiE4hZBN/rndG1On+OXyKAaSQ=',
            'Authorization': f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="OEC3RHh/Ey/QD1t6mDspqLD2xw+LsNgpkFyiRucbN3ps8t0/ko//zugE+wf36adPa4088cETicPf2ztLJaoUq39/+L0mGco+ztLDXFwN2Iu7FQveq5GZ7bfMhrz/RTeqQ5VlGA5Bs570qYyioz1eN5uR4pEMDT1X5mdAuAVQf2mH+AFupPxjxWh8KMr4hd1y9zD4ivnbZqAPUmX8FMJbrt+i2n9ZbSsuGD6cqDtYOCsG8Mu8aDDx148W94Ik+eyhutXjHK6YO0aTtsnLhN4JVJrFsC3sIJZc2A1gUSDRIQbiqmFWPx5cyP/HYUnPPVU2oCE9dXtTJYKFoflXm4YThF1DHFJBexKI6siqnSeT+VqopwDg7iD2k3CzEujK4SrviINdgwn0M5n1gBwmJED0Juj0zRbVZOk+cwHnebFgp+9HjW0zhgcE0uSiviFNnicBD7t7QVKYdTN09e9JUSmV9C+wjE+umF9Kkk9ZYe4AL6K9p9tYafGMZ1hzktSV/EfCLi440hNxC/b6kheAEegVnHhQa4gdHscVBL1m7nVJm1UmbnfYaf313XdXXyeRz1/DxP7vlK6Z5jenIkEWCaiJfwFKp+EmVfdh7p74URivbYp8IK7hauY27c9BWZheSCATDlrSrgvXrhILWPBw8g8OIKfWgH+x4HKjtrJ6parAjW8="'
        }.items()

class TestGetPaymentDetails:

    @responses.activate
    @freeze_time('Mon, 18 Mar 2019 15:10:24 +0000')
    def test_staging(self, key_id, key, payment_id):
        responses.add(responses.GET, f'https://staging.authservices.satispay.com/g_business/v1/payments/{payment_id}', body='{}', status=200)
        response = satispaython.get_payment_details(key_id, key, payment_id, True)
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'GET'
        assert request.body == None
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Host': 'staging.authservices.satispay.com',
            'Date': 'Mon, 18 Mar 2019 15:10:24 +0000',
            'Digest': 'SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=',
            'Authorization': f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="ZhkBZSOvVBoB4/inTKc4j9daeDhii6xc22mfLurTc8KvDQiGu6eGxaOFfmgSFrEWGbQ3ZJsLP4E1Nh6K5vCvuiUqVZzVVtiC8LI6rdOHieYPoCRCgJ2wgJUPC4azU/pzlDnZcZOzjEJIHp0j3m8Sn/86ibMzpueoF7IZjquhp+tMom702kK2yzxgDfAK7Ug5yjS87m/APbMZMVnuCZtZt0K/21hBXQs6upge5q7j7sR24usJqW446VSNkE70KUfj3ymqa+iftcocAgyvTUYcz6Sf9vycanCip6f4la5j93WPBRl3e0VtVYRgomaHM6vwbnJwu5/5F/xjX3JWaEO0UpLVJr4oK7GV1tD5610Z+P5XLVRyCAIXZxHd7eKAnTE/9Lg5mOMQ2pEwHwGzghMdm857ZplZngnH4yeKv1TVBni5p/7tkW+Cle2VWtn+1E+uonlX1tc+48GgWp3XstYES03i4ClUWBHetj1J5ti0+3reW0xOeomcXD4fcdpwXSyC0S7NDjHKqwnzEfUVD9lZgsJKP8Y+N2wTRcjPZbM6sLj8nmM6SPFgFaYCCubnmucZxf9pVoX4PN46Ad8RFaAzlykRd2GnleNIxtqG2TdTnYn53eEffcEDw9/7IuRrn/JnbjeatN81cIdqTuaJWypGaaMg+NPr//gyuE5eU8vH56I="'
        }.items()

    @responses.activate
    @freeze_time('Mon, 18 Mar 2019 15:10:24 +0000')
    def test_production(self, key_id, key, payment_id):
        responses.add(responses.GET, f'https://authservices.satispay.com/g_business/v1/payments/{payment_id}', body='{}', status=200)
        response = satispaython.get_payment_details(key_id, key, payment_id)
        request = responses.calls[0].request
        assert len(responses.calls) == 1
        assert request.method == 'GET'
        assert request.body == None
        assert request.headers.items() >= {
            'Accept': 'application/json',
            'Host': 'authservices.satispay.com',
            'Date': 'Mon, 18 Mar 2019 15:10:24 +0000',
            'Digest': 'SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=',
            'Authorization': f'Signature keyId="{key_id}", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="YQDOUhmUou6hk1G4Hs00/3QXiblkPItg5OYEIrgNGh/6amBYcsOOm7m5lR7ar1AG2Ys5945eDfwByaRLDiK9l9L0s7KxOPpEDX1cxVHy65gcvSUZtg1OvHFygaPse2H91XTjaK2DPytpF59+vhKovR37RuPyAISMkDjlG2ZBSfc0GGFRMjv00xqrAs/ryWaaZjhp4mrcwp8OlUKKNXCHF2WDIZr8lcEBvWnavAVwJn8FIxFmZ1bbWNszEnqz1l4ub0+bmTrYoXw7VHXV7v28F0hAcBl8LtXCJWRh9LzcpdMN038Vf7VDCuLAN8Vhrh1srdZEjH1vebdIlVC1QUfCK1vfbr9BEr9ZAmZXGLzZagTNZpAoIm9Zc2RfB+XPzKub61AGKU06TU/dDaNIs9kVl2QBKdtMLXWX2YBqRVkKcRF7x8f7ESdgNk+kJ9GzFxGSHbomt9ObeHqDJiR2GPgVFIj/LtwhBxuq69AmRZcMEf6/AoulHUWasZl1r0aidBY45HmB9uAzbcWmzjoKI/S2K18FUUAFohQ2Dx+K6zHwuXOGkKXYaxBXRc4C5DrhXB5P+iyyQm6qdoylzu/DOw6dmNNAoeth82FYPGkL2PfJC1YHFspkf+zMDzuVqpSrKL78pNIByBif2+G91PZyXvTW178rD09pCia3YSlqfd3IMSI="'
        }.items()
