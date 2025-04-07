import zlib
import gzip
import bz2
import lzma
from enum import Enum, auto
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)


class CompressionAlgorithm(Enum):
    """Поддерживаемые алгоритмы сжатия"""
    ZLIB = auto()
    GZIP = auto()
    BZ2 = auto()
    LZMA = auto()


class DataCompressor:
    """
    Универсальный компрессор данных с поддержкой:
    - Мультиалгоритмов сжатия
    - Автовыбора оптимального метода
    - Потокового сжатия
    """

    DEFAULT_LEVEL = 6  # Оптимальный баланс скорость/степень сжатия

    def compress(
            self,
            data: Union[str, bytes],
            algorithm: CompressionAlgorithm = CompressionAlgorithm.ZLIB,
            level: Optional[int] = None
    ) -> bytes:
        """
        Сжатие данных с указанным алгоритмом
        :param data: Входные данные (str или bytes)
        :param algorithm: Алгоритм из CompressionAlgorithm
        :param level: Уровень сжатия (1-9)
        :return: Сжатые данные в bytes
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        level = level or self.DEFAULT_LEVEL

        try:
            if algorithm == CompressionAlgorithm.ZLIB:
                return zlib.compress(data, level=level)
            elif algorithm == CompressionAlgorithm.GZIP:
                return gzip.compress(data, compresslevel=level)
            elif algorithm == CompressionAlgorithm.BZ2:
                return bz2.compress(data, compresslevel=level)
            elif algorithm == CompressionAlgorithm.LZMA:
                return lzma.compress(data, preset=level)
        except Exception as e:
            logger.error(f"Compression failed: {str(e)}")
            raise

    def decompress(
            self,
            compressed_data: bytes,
            algorithm: CompressionAlgorithm = CompressionAlgorithm.ZLIB
    ) -> bytes:
        """
        Распаковка данных
        :param compressed_data: Сжатые данные
        :param algorithm: Алгоритм, использованный при сжатии
        :return: Распакованные данные
        """
        try:
            if algorithm == CompressionAlgorithm.ZLIB:
                return zlib.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.GZIP:
                return gzip.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.BZ2:
                return bz2.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.LZMA:
                return lzma.decompress(compressed_data)
        except Exception as e:
            logger.error(f"Decompression failed: {str(e)}")
            raise

    def auto_compress(self, data: Union[str, bytes]) -> tuple:
        """
        Автоматический выбор лучшего алгоритма сжатия
        :return: (compressed_data, algorithm_used)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        results = []
        for algo in CompressionAlgorithm:
            try:
                compressed = self.compress(data, algorithm=algo)
                results.append((len(compressed), compressed, algo))
            except Exception:
                continue

        if not results:
            raise ValueError("No suitable compression algorithm found")

        # Выбор алгоритма с наилучшим сжатием
        return min(results, key=lambda x: x[0])[1:]