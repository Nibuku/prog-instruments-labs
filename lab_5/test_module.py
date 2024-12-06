import os

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from open_save_part import read_file, write_data
import cryptography_part as cp
from symmetric import Action, encrypt_decrypt


@pytest.fixture
def rsa_keys():
    """Создаем тестовые RSA-ключи для шифрования и расшифровки."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.mark.parametrize("key_size", [8, 16, 24])
def test_encrypt(rsa_keys, key_size):
    """Тестируем шифрование с использованием публичного ключа."""
    private_key, public_key = rsa_keys
    symmetric_key = os.urandom(key_size)

    encrypted_data = encrypt_decrypt(public_key, symmetric_key, Action.ENCRYPT)

    assert encrypted_data != symmetric_key
    assert isinstance(encrypted_data, bytes)


@pytest.mark.parametrize("key_size", [8, 16, 24])
def test_decrypt(rsa_keys, key_size):
    """Тест расшифровки с использованием приватного ключа."""
    private_key, public_key = rsa_keys
    symmetric_key = os.urandom(key_size)
    encrypted_data = encrypt_decrypt(public_key, symmetric_key, Action.ENCRYPT)
    decrypted_data = encrypt_decrypt(private_key, encrypted_data, Action.DECRYPT)
    assert decrypted_data == symmetric_key


@pytest.mark.parametrize("key_size", [8, 16, 24])
def test_invalid_action(rsa_keys, caplog, key_size):
    """Cлучай с некорректным значением действия."""
    private_key, public_key = rsa_keys
    symmetric_key = os.urandom(key_size)
    with pytest.raises(ValueError, match="Invalid action provided"):
        encrypt_decrypt(public_key, symmetric_key, "INVALID_ACTION")
        assert "The parameter is not specified" in caplog.text


@pytest.fixture
def cryptography_instance():
    """Создание экземпляра Cryptograthy для тестирования."""
    return cp.Cryptograthy(
        symmetric_key=os.path.join("lab_5", "keys", "sym.txt"),
        private_key=os.path.join("lab_5", "keys", "priv.pem"),
        public_key=os.path.join("lab_5", "keys", "pub.pem"),
        key_size=8,
    )


def test_key_generation(cryptography_instance):
    """Тестируем генерацию ключей."""
    cryptography_instance.key_generation()
    assert os.path.exists(cryptography_instance.symmetric_key)
    assert os.path.exists(cryptography_instance.private_key)
    assert os.path.exists(cryptography_instance.public_key)

    for file_path in [
        cryptography_instance.symmetric_key,
        cryptography_instance.private_key,
        cryptography_instance.public_key,
    ]:
        with open(file_path, "rb") as file:
            file_content = file.read()
            assert len(file_content) > 0


def test_encryption(cryptography_instance):
    """Тестирование шифрования текста"""
    cryptography_instance.encryption(
        os.path.join("lab_5", "text", "base_text.txt"),
        os.path.join( "lab_5", "text", "shifr_text.txt"),
    )
    assert os.path.exists(
        os.path.join("lab_5", "text", "shifr_text.txt")
    )

    encrypted_data = read_file(
        os.path.join("lab_5", "text", "shifr_text.txt")
    )
    original_data = read_file(
        os.path.join("lab_5", "text", "base_text.txt")
    )
    assert encrypted_data != original_data
    assert len(encrypted_data) > len(original_data)


def test_decryption(cryptography_instance):
    """Тестирование расшифровки зашифрованного текста"""
    encrypted_file_path = os.path.join("lab_5", "text", "shifr_text.txt"
    )
    decrypted_file_path = os.path.join("lab_5", "text", "deshifr_text.txt"
    )
    original_file_path = os.path.join( "lab_5", "text", "base_text.txt"
    )

    cryptography_instance.decryption(encrypted_file_path, decrypted_file_path)
    assert os.path.exists(decrypted_file_path)
    encrypted_data = read_file(encrypted_file_path)
    decrypted_data = read_file(decrypted_file_path)
    original_data = read_file(original_file_path)

    assert (
        decrypted_data == original_data
    ), "Decrypted data does not match the original data."
    assert (
        decrypted_data != encrypted_data
    ), "Decrypted data should not be the same as the encrypted data."


def test_write_data(mocker):
    """Тестирование функции записи данных"""
    test_data = os.urandom(8)
    file_path = "test_path.txt"
    mock_file = mocker.patch("builtins.open", mocker.mock_open())
    write_data(file_path, test_data)

    mock_file.assert_called_once_with(file_path, "wb")
    mock_file().write.assert_called_once_with(test_data)


def test_read_file(mocker):
    """Тестирование функции чтения"""
    test_data = os.urandom(8)
    file_path = "test_path.txt"
    mock_file = mocker.patch("builtins.open", mocker.mock_open())
    mock_file.return_value.__enter__.return_value.read.return_value = test_data
    result = read_file(file_path)

    mock_file.assert_called_once_with(file_path, "rb")
    assert result == test_data
