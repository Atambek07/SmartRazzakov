import trimesh
import numpy as np
from io import BytesIO
from .exceptions import ModelOptimizationError
import logging

logger = logging.getLogger(__name__)


class ModelProcessor:
    def optimize(self, model_path: str, target: str = 'web') -> BytesIO:
        """Оптимизация модели для целевой платформы"""
        try:
            mesh = trimesh.load(model_path)

            if target == 'web':
                return self._optimize_for_web(mesh)
            elif target == 'ar':
                return self._optimize_for_ar(mesh)
            else:
                raise ModelOptimizationError(f"Unknown target: {target}")

        except Exception as e:
            logger.error(f"3D processing error: {str(e)}")
            raise ModelOptimizationError("Model optimization failed")

    def _optimize_for_web(self, mesh) -> BytesIO:
        """Оптимизация для веб-приложений"""
        mesh = mesh.simplify_quadratic_decimation(5000)
        buffer = BytesIO()
        mesh.export(buffer, file_type='glb')
        buffer.seek(0)
        return buffer

    def _optimize_for_ar(self, mesh) -> BytesIO:
        """Оптимизация для AR-приложений"""
        mesh = mesh.simplify_quadratic_decimation(2000)
        mesh.apply_scale(0.1)  # Нормализация размера
        buffer = BytesIO()
        mesh.export(buffer, file_type='glb')
        buffer.seek(0)
        return buffer


