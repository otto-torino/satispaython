from datetime import datetime

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from pytest import fixture, raises

from satispaython.utils.utils import format_datetime, generate_key, load_key, write_key


@fixture()
def key_path(tmp_path_factory):
    path = tmp_path_factory.getbasetemp().joinpath("test.pem")
    yield path
    path.unlink()


class TestDateUtils:
    def test_format_datetime(self):
        date = datetime(2020, 1, 1)
        assert format_datetime(date) == "2020-01-01T00:00:00.000Z"


class TestKeyUtils:
    class TestGenerateKey:
        def test_generate_key(self):
            rsa_key = generate_key()
            assert rsa_key.private_numbers().public_numbers.e == 65537
            assert rsa_key.key_size == 4096

        def test_generate_key_with_path(self, rsa_key, key_path):
            rsa_key = generate_key(key_path)
            assert rsa_key.private_numbers().public_numbers.e == 65537
            assert rsa_key.key_size == 4096
            assert key_path.exists()
            with open(key_path, "rb") as file:
                rsa_key = load_pem_private_key(file.read(), None)
                assert rsa_key.private_numbers().public_numbers.e == 65537
                assert rsa_key.key_size == 4096

        def test_generate_key_with_password(self, rsa_key, key_path):
            rsa_key = generate_key(key_path, "password")
            assert rsa_key.private_numbers().public_numbers.e == 65537
            assert rsa_key.key_size == 4096
            assert key_path.exists()
            with open(key_path, "rb") as file:
                rsa_key = load_pem_private_key(file.read(), b"password")
                assert rsa_key.private_numbers().public_numbers.e == 65537
                assert rsa_key.key_size == 4096

    class TestWriteKey:
        def test_write_key(self, rsa_key, key_path):
            write_key(rsa_key, key_path)
            assert key_path.exists()
            with open(key_path, "rb") as file:
                rsa_key = load_pem_private_key(file.read(), None)
                assert rsa_key.private_numbers().public_numbers.e == 65537
                assert rsa_key.key_size == 4096

        def test_write_key_with_password(self, rsa_key, key_path):
            write_key(rsa_key, key_path, "password")
            assert key_path.exists()
            with open(key_path, "rb") as file:
                rsa_key = load_pem_private_key(file.read(), b"password")
                assert rsa_key.private_numbers().public_numbers.e == 65537
                assert rsa_key.key_size == 4096

    class TestLoadKey:
        def test_load_unencrypted_key(self, rsa_key, key_path):
            write_key(rsa_key, key_path)
            rsa_key = load_key(key_path)
            assert rsa_key.private_numbers().public_numbers.e == 65537
            assert rsa_key.key_size == 4096

        def test_load_encrypted_key_with_password(self, rsa_key, key_path):
            write_key(rsa_key, key_path, "password")
            rsa_key = load_key(key_path, "password")
            assert rsa_key.private_numbers().public_numbers.e == 65537
            assert rsa_key.key_size == 4096

        def test_load_unencrypted_key_with_password(self, rsa_key, key_path):
            write_key(rsa_key, key_path)
            with raises(TypeError):
                load_key(key_path, "password")

        def test_load_encrypted_key_without_password(self, rsa_key, key_path):
            write_key(rsa_key, key_path, "password")
            with raises(TypeError):
                load_key(key_path)

        def test_load_encrypted_key_with_wrong_password(self, rsa_key, key_path):
            write_key(rsa_key, key_path, "password")
            with raises(ValueError):
                load_key(key_path, "wrong_password")
