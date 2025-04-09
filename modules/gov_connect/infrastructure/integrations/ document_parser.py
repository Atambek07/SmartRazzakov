# modules/gov_connect/infrastructure/integrations/document_parser.py
from abc import ABC, abstractmethod
from io import BytesIO
import logging
from typing import Optional
import pytesseract
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
from PIL import Image

logger = logging.getLogger(__name__)

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, content: bytes, file_type: str) -> str:
        pass

class PDFParser(DocumentParser):
    def parse(self, content: bytes, file_type: str = 'pdf') -> str:
        try:
            # Парсинг текстовых PDF
            text = extract_text(BytesIO(content))
            if text.strip():
                return text
            
            # Обработка сканированных PDF через OCR
            images = convert_from_bytes(content)
            return '\n'.join(pytesseract.image_to_string(img) for img in images)
            
        except Exception as e:
            logger.error(f"PDF parsing error: {str(e)}")
            raise ValueError("Invalid PDF format") from e

class ImageOCRParser(DocumentParser):
    SUPPORTED_TYPES = {'png', 'jpg', 'jpeg', 'tiff'}
    
    def parse(self, content: bytes, file_type: str) -> str:
        if file_type.lower() not in self.SUPPORTED_TYPES:
            raise ValueError(f"Unsupported image type: {file_type}")
        
        try:
            image = Image.open(BytesIO(content))
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"OCR processing error: {str(e)}")
            raise ValueError("Image processing failed") from e