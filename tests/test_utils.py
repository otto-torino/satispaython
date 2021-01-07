from pytest import fixture, raises
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from satispaython.utils import generate_key, write_key, load_key, format_datetime


@fixture(scope='module')
def key_path(tmp_path_factory):
    return tmp_path_factory.getbasetemp().joinpath('test.pem')


class Test_Date_Utils:

    def test_format_datetime(self):
        date = datetime(2020, 1, 1)
        assert format_datetime(date) == '2020-01-01T00:00:00.000Z'


class Test_Key_Utils:

    class Test_Generate_Key:

        def test_generate_key(self):
            key = generate_key()
            assert key.private_numbers().public_numbers.e == 65537
            assert key.key_size == 4096

    class Test_Write_Key:

        def test_write_key(self, key, key_path):
            write_key(key, key_path)
            assert key_path.exists()
            with open(key_path, 'rb') as file:
                key = serialization.load_pem_private_key(file.read(), None)
                assert key.private_numbers().public_numbers.e == 65537
                assert key.key_size == 4096

        def test_write_key_with_password(self, key, key_path):
            write_key(key, key_path, 'password')
            assert key_path.exists()
            with open(key_path, 'rb') as file:
                data = file.read()
                key = serialization.load_pem_private_key(data, b'password')
                assert key.private_numbers().public_numbers.e == 65537
                assert key.key_size == 4096

    class Test_Load_Key:

        def test_load_unencrypted_key(self, key, key_path):
            write_key(key, key_path)
            key = load_key(key_path)
            assert key.private_numbers().public_numbers.e == 65537
            assert key.key_size == 4096

        def test_load_encrypted_key_with_password(self, key, key_path):
            write_key(key, key_path, 'password')
            key = load_key(key_path, 'password')
            assert key.private_numbers().public_numbers.e == 65537
            assert key.key_size == 4096

        def test_load_unencrypted_key_with_password(self, key, key_path):
            write_key(key, key_path)
            with raises(TypeError):
                load_key(key_path, 'password')

        def test_load_encrypted_key_without_password(self, key, key_path):
            write_key(key, key_path, 'password')
            with raises(TypeError):
                load_key(key_path)

        def test_load_encrypted_key_with_wrong_password(self, key, key_path):
            write_key(key, key_path, 'password')
            with raises(ValueError):
                load_key(key_path, 'wrong_password')
