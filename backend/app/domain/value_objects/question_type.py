from enum import Enum


class QuestionType(str, Enum):
    SELECCION_MULTIPLE = "seleccion_multiple"
    VERDADERO_FALSO = "verdadero_falso"
    DESARROLLO = "desarrollo"
    EMPAREJAMIENTO = "emparejamiento"
