from enum import Enum
from typing import List


class TypesEstudiante(Enum):
    SEDE_AMAZONIA = "SEDE AMAZONÍA"
    SEDE_BOGOTA = "SEDE BOGOTÁ"
    SEDE_CARIBE = "SEDE CARIBE"
    SEDE_DE_LA_PAZ = "SEDE DE LA PAZ"
    SEDE_MANIZALES = "SEDE MANIZALES"
    SEDE_MEDELLÍN = "SEDE MEDELLÍN"
    SEDE_ORINOQUÍA = "SEDE ORINOQUÍA"
    SEDE_PALMIRA = "SEDE PALMIRA"
    SEDE_TUMACO = "SEDE TUMACO"


class EstudianteActivos(Enum):
    NOMBRES_APELLIDOS = 1
    EMAIL = 2
    SEDE = 3
    FACULTAD = 4
    COD_PLAN = 5
    PLAN = 6
    TIPO_NIVEL = 7

    @classmethod
    def validate_headers(cls, headers: List[str]) -> bool:
        """
        Verifica si todos los encabezados en `headers` están en el Enum.
        No requiere que estén en orden, pero sí que estén todos presentes.
        """
        # Normalizamos las cadenas para evitar errores por
        # mayúsculas/minúsculas/espacios

        normalized_headers = {h.strip().upper() for h in headers if h}
        enum_headers = {e.name for e in cls}
        return enum_headers.issubset(normalized_headers)
