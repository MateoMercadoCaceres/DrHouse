from enum import Enum

class SeverityLevel(str, Enum):
    """
    Enum for disease severity levels
    """
    LEVE = "leve"
    MODERADO = "moderado"
    GRAVE = "grave"
    CRITICO = "critico" 