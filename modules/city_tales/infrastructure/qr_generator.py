from qrcode.image.styledpil import StyledPilmage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

class CustomQRGenerator:
    """Генератор стилизованных QR-кодов для брендинга."""

    @staticmethod
    def generate_branded_qr(
        data: str,
        logo_path: str,
        output_path: str = None
    ) -> bytes:
        """Создает QR-код с логотипом и градиентом."""
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                center_color=(70, 130, 180),  # SteelBlue
                edge_color=(25, 25, 112)     # MidnightBlue
            )
        )

        # Добавление логотипа
        logo = Image.open(logo_path)
        img.paste(logo, (img.size[0]//4, img.size[1]//4, img.size[0]//4*3, img.size[1]//4*3))

        if output_path:
            img.save(output_path)
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()