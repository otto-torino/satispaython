from pytest import fixture
from cryptography.hazmat.primitives import serialization


@fixture
def date():
    return 'Mon, 18 Mar 2019 15:10:24 +0000'

@fixture(scope='session')
def key():
    with open('key.pem', 'rb') as file:
        yield serialization.load_pem_private_key(file.read(), None)

@fixture()
def mock_date(monkeypatch, date):
    monkeypatch.setattr('satispaython._core.get_formatted_date', lambda: date)
