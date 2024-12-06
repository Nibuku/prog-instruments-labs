import pytest
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import asymmetric, hashes
from cryptography.hazmat.primitives import serialization, padding
from symmetric import encrypt_decrypt, Action


@pytest.fixture
def rsa_keys():
    """Создаем тестовые RSA-ключи для шифрования и расшифровки."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def test_encrypt(rsa_keys):
    """Тестируем шифрование с использованием публичного ключа."""
    private_key, public_key = rsa_keys
    symmetric_key = os.urandom(8)

    encrypted_data = encrypt_decrypt(public_key, symmetric_key, Action.ENCRYPT)

    assert encrypted_data != symmetric_key
    assert isinstance(encrypted_data, bytes)


def test_decrypt(rsa_keys):
    """Тестируем расшифровку с использованием приватного ключа."""
    private_key, public_key = rsa_keys
    symmetric_key = os.urandom(8)
    encrypted_data = encrypt_decrypt(public_key, symmetric_key, Action.ENCRYPT)
    decrypted_data = encrypt_decrypt(private_key, encrypted_data, Action.DECRYPT)
    assert decrypted_data == symmetric_key


def test_invalid_action(rsa_keys):
    """Тестируем случай с некорректным значением действия."""
    private_key, public_key = rsa_keys
    symmetric_key = b"test_symmetric_key"

    with pytest.raises(ValueError):
        encrypt_decrypt(public_key, symmetric_key, "INVALID_ACTION")