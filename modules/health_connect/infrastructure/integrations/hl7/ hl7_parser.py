# modules/health_connect/infrastructure/integrations/hl7/hl7_parser.py
import re
from datetime import datetime
from typing import Dict, List, Union
from loguru import logger

class HL7ParseError(Exception):
    """Ошибка парсинга HL7 сообщения"""

class HL7Parser:
    def __init__(self, encoding: str = 'UTF-8'):
        self.encoding = encoding
        self.segment_regex = re.compile(r'[\r\n]+')
        self.field_regex = re.compile(r'\|')
        self.component_regex = re.compile(r'\^')
        self.subcomponent_regex = re.compile(r'&')
    
    def parse(self, message: str) -> Dict[str, List[List[Union[str, dict]]]]:
        """Парсинг HL7 v2.x сообщения в структурированный формат"""
        try:
            segments = self.segment_regex.split(message.strip())
            parsed_message = {}
            
            for segment in segments:
                if not segment:
                    continue
                
                fields = self.field_regex.split(segment)
                segment_name = fields[0]
                parsed_fields = []
                
                for field in fields[1:]:
                    components = self.component_regex.split(field)
                    subcomponents = [self.subcomponent_regex.split(c) for c in components]
                    parsed_fields.append(subcomponents)
                
                parsed_message.setdefault(segment_name, []).append(parsed_fields)
            
            self._validate_message(parsed_message)
            return parsed_message
        
        except Exception as e:
            logger.error(f"HL7 parsing failed: {str(e)}")
            raise HL7ParseError(f"Invalid HL7 message: {str(e)}") from e

    def serialize(self, data: Dict) -> str:
        """Сериализация структурированных данных в HL7 формат"""
        segments = []
        for segment_name, instances in data.items():
            for instance in instances:
                fields = [segment_name]
                for field in instance:
                    components = ['^'.join('&'.join(sc) for sc in component) 
                                for component in field]
                    fields.append('|'.join(components))
                segments.append('\r'.join(fields))
        return '\r'.join(segments)

    def _validate_message(self, parsed: Dict):
        """Базовая валидация структуры сообщения"""
        if 'MSH' not in parsed:
            raise HL7ParseError("Missing MSH segment")
        
        msh_segment = parsed['MSH'][0][0]
        if len(msh_segment) < 12:
            raise HL7ParseError("Invalid MSH segment structure")

class HL7ClinicalDataConverter:
    """Конвертер клинических данных в стандартные модели"""
    
    def convert_patient(self, hl7_data: Dict) -> Dict:
        """Преобразование данных пациента из сегментов PID"""
        pid = hl7_data.get('PID', [])[0][0]
        return {
            'id': self._get_field(pid, 3),
            'name': self._parse_name(self._get_field(pid, 5)),
            'birth_date': self._parse_date(self._get_field(pid, 7)),
            'gender': self._get_field(pid, 8),
            'address': self._parse_address(self._get_field(pid, 11))
        }

    def _parse_name(self, components: List) -> Dict:
        return {
            'family': components[0][0],
            'given': components[0][1:3],
            'suffix': components[0][3] if len(components[0]) > 3 else None
        }

    def _parse_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, '%Y%m%d') if date_str else None

    def _parse_address(self, components: List) -> Dict:
        return {
            'street': components[0][0],
            'city': components[0][2],
            'state': components[0][3],
            'postal_code': components[0][4],
            'country': components[0][5]
        }

    def _get_field(self, segment: List, index: int) -> Union[str, List]:
        try:
            return segment[index-1] if index-1 < len(segment) else None
        except IndexError:
            return None