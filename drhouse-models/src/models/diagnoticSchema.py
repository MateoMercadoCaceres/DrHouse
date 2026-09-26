from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SeverityLevel(str, Enum):
    LEVE = "leve"
    MODERADO = "moderado"
    GRAVE = "grave"
    CRITICO = "crítico"

class UserInputRequest(BaseModel):
    user_input: str = Field(..., description="Descripción de los síntomas en lenguaje natural", example="Me duele mucho la cabeza y tengo fiebre alta desde ayer")

class DiagnosisRequest(BaseModel):
    diagnosis: str = Field(..., description="Nombre de la enfermedad o diagnóstico", example="migraña")

class SymptomsResponse(BaseModel):
    symptoms: List[str] = Field(..., description="Lista de síntomas identificados")
    user_input: str = Field(..., description="Entrada original del usuario")

class DiagnosticResponse(BaseModel):
    symptoms: List[str] = Field(..., description="Lista de síntomas identificados")
    initial_diagnosis: str = Field(..., description="Diagnóstico inicial", example="No definido")
    final_diagnosis: str = Field(..., description="Diagnóstico final o mejorado")
    user_input: str = Field(..., description="Entrada original del usuario")

class DiseaseExplanationResponse(BaseModel):
    disease_name: str = Field(..., description="Nombre de la enfermedad")
    description: str = Field(..., description="Descripción detallada de la enfermedad")
    severity: SeverityLevel = Field(..., description="Nivel de gravedad de la enfermedad")
    treatment_recommendations: List[str] = Field(..., description="Recomendaciones de tratamiento generales")

class APIInfoResponse(BaseModel):
    name: str = Field(..., description="Nombre de la API")
    version: str = Field(..., description="Versión de la API")
    description: str = Field(..., description="Descripción de la funcionalidad")
    endpoints: List[str] = Field(..., description="Lista de endpoints disponibles")
    powered_by: str = Field(..., description="Tecnología utilizada")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Descripción del error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")