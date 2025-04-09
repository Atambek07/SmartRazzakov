# modules/health_connect/infrastructure/integrations/hl7/fhir_adapter.py
from typing import Dict, Any
from fhir.resources import construct_fhir_element
from loguru import logger

class FHIRConversionError(Exception):
    """Ошибка преобразования в FHIR формат"""

class FHIRAdapter:
    def __init__(self, fhir_version: str = 'R4'):
        self.fhir_version = fhir_version
    
    def hl7_to_fhir(self, hl7_data: Dict, resource_type: str) -> Dict:
        """Преобразование HL7 v2.x данных в FHIR ресурс"""
        try:
            converter_method = getattr(self, f'_convert_to_{resource_type.lower()}')
            return converter_method(hl7_data)
        except AttributeError:
            raise FHIRConversionError(f"Unsupported resource type: {resource_type}")

    def fhir_to_hl7(self, fhir_resource: Dict) -> Dict:
        """Преобразование FHIR ресурса в HL7 v2.x формат"""
        resource_type = fhir_resource['resourceType']
        try:
            converter_method = getattr(self, f'_convert_from_{resource_type.lower()}')
            return converter_method(fhir_resource)
        except AttributeError:
            raise FHIRConversionError(f"Unsupported FHIR resource: {resource_type}")

    def _convert_to_patient(self, hl7_data: Dict) -> Dict:
        """Создание FHIR Patient из HL7 PID сегмента"""
        patient = construct_fhir_element('Patient', {})
        pid = hl7_data.get('PID', [])[0][0]
        
        # Преобразование имени
        name = patient.name = [construct_fhir_element('HumanName', {})]
        name[0].family = self._get_hl7_field(pid, 5, 0, 0)
        name[0].given = [self._get_hl7_field(pid, 5, 0, 1)]
        
        # Преобразование даты рождения
        birth_date = self._get_hl7_field(pid, 7)
        if birth_date:
            patient.birthDate = birth_date
        
        # Преобразование пола
        gender_map = {'M': 'male', 'F': 'female', 'U': 'unknown'}
        patient.gender = gender_map.get(self._get_hl7_field(pid, 8), 'unknown')
        
        return patient.dict()

    def _convert_from_patient(self, patient: Dict) -> Dict:
        """Преобразование FHIR Patient в HL7 формат"""
        hl7_message = {'PID': [[]]}
        pid = hl7_message['PID'][0]
        
        # Идентификатор пациента
        pid.append([[patient['id']]])
        
        # Имя
        name = patient.get('name', [{}])[0]
        pid.append([[
            name.get('family', ''),
            name.get('given', [''])[0],
            '',  # Middle name
            name.get('suffix', '')
        ]])
        
        # Дата рождения
        pid.append([[patient.get('birthDate', '')]])
        
        # Пол
        gender_map = {'male': 'M', 'female': 'F', 'unknown': 'U'}
        pid.append([[gender_map.get(patient.get('gender', 'unknown'), 'U')]])
        
        return hl7_message

    def _get_hl7_field(self, segment: List, 
                     field_idx: int, 
                     component_idx: int = 0, 
                     subcomponent_idx: int = 0) -> str:
        """Извлечение данных из HL7 структуры"""
        try:
            return segment[field_idx-1][component_idx][subcomponent_idx]
        except (IndexError, KeyError):
            return ''

class FHIRClinicalDataMapper:
    """Расширенный маппинг клинических данных"""
    
    def map_observation(self, hl7_data: Dict) -> Dict:
        """Преобразование OBX сегментов в FHIR Observation"""
        observations = []
        for obx in hl7_data.get('OBX', []):
            observation = construct_fhir_element('Observation', {
                "status": "final",
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": self._get_field(obx, 3, 0, 0)
                    }]
                },
                "valueQuantity": {
                    "value": self._get_field(obx, 5, 0, 0),
                    "unit": self._get_field(obx, 6, 0, 0)
                }
            })
            observations.append(observation.dict())
        return observations

    def map_condition(self, hl7_data: Dict) -> Dict:
        """Преобразование DG1 сегментов в FHIR Condition"""
        conditions = []
        for dg1 in hl7_data.get('DG1', []):
            condition = construct_fhir_element('Condition', {
                "code": {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": self._get_field(dg1, 3, 0, 0)
                    }]
                },
                "onsetDateTime": self._parse_hl7_date(
                    self._get_field(dg1, 5)
                )
            })
            conditions.append(condition.dict())
        return conditions

    def _parse_hl7_date(self, date_str: str) -> str:
        """Преобразование даты из HL7 формата в FHIR"""
        if len(date_str) >= 8:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return None