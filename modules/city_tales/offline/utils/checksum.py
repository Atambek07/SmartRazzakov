import hashlib
from typing import Union, Optional
import logging
from enum import Enum, auto

logger = logging.getLogger(__name__)


class HashAlgorithm(Enum):
    """Поддерживаемые алгоритмы хеширования"""
    MD5 = auto()
    SHA1 = auto()
    SHA256 = auto()
    BLAKE2 = auto()


class IntegrityChecker:
    """
    Проверка целостности данных с помощью:
    - Контрольных сумм
    - Цифровых подписей
    - Верификации файлов
    """

    CHUNK_SIZE = 65536  # Для потокового чтения больших файлов

    def calculate_hash(
            self,
            data: Union[str, bytes, bytearray],
            algorithm: HashAlgorithm = HashAlgorithm.SHA256,
            return_hex: bool = True
    ) -> Union[str, bytes]:
        """
        Расчет хеш-суммы для данных
        :param data: Входные данные
        :param algorithm: Алгоритм хеширования
        :param return_hex: Возвращать hex-строку или сырые байты
        :return: Хеш-сумма
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        hash_obj = self._get_hash_object(algorithm)
        hash_obj.update(data)

        return hash_obj.hexdigest() if return_hex else hash_obj.digest()

    def verify_hash(
            self,
            data: Union[str, bytes],
            expected_hash: str,
            algorithm: HashAlgorithm = HashAlgorithm.SHA256
    ) -> bool:
        """
        Проверка соответствия данных ожидаемой хеш-сумме
        :param expected_hash: Ожидаемый хеш в hex-формате
        :return: True если хеши совпадают
        """
        actual_hash = self.calculate_hash(data, algorithm, True)
        return actual_hash == expected_hash.lower()

    def calculate_file_hash(
            self,
            file_path: str,
            algorithm: HashAlgorithm = HashAlgorithm.SHA256,
            return_hex: bool = True
    ) -> Union[str, bytes]:
        """
        Потоковый расчет хеша для файла
        """
        hash_obj = self._get_hash_object(algorithm)

        with open(file_path, 'rb') as f:
            while chunk := f.read(self.CHUNK_SIZE):
                hash_obj.update(chunk)

        return hash_obj.hexdigest() if return_hex else hash_obj.digest()

    def _get_hash_object(self, algorithm: HashAlgorithm):
        """Создание объекта хеширования"""
        if algorithm == HashAlgorithm.MD5:
            return hashlib.md5()
        elif algorithm == HashAlgorithm.SHA1:
            return hashlib.sha1()
        elif algorithm == HashAlgorithm.SHA256:
            return hashlib.sha256()
        elif algorithm == HashAlgorithm.BLAKE2:
            return hashlib.blake2b()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")