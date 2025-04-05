import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


class QRCodeService:
    @staticmethod
    def generate_qr_code(url: str) -> File:
        """Генерирует QR-код и возвращает как Django File"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)

        return File(buffer, name=f"qr_{hash(url)}.png")