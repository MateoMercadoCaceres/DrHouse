from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from enum import Enum

class DiagnosticMode(str, Enum):
    DIAGNOSE = "diagnose"
    SYMPTOMS = "symptoms"
    EXPLAIN = "explain"

class DiagnosticRequest(BaseModel):
    user_input: str
    mode: DiagnosticMode = Field(default=DiagnosticMode.DIAGNOSE, description="Modalidad de diagnóstico")

class SymptomsRequest(BaseModel):
    user_input: str

class ExplainDiseaseRequest(BaseModel):
    diagnosis: str

# Respuestas de la API externa
class DiagnosticAPIResponse(BaseModel):
    symptoms: List[str]
    initial_diagnosis: str
    final_diagnosis: str
    user_input: str

class SymptomsAPIResponse(BaseModel):
    symptoms: List[str]
    user_input: str

class ExplainDiseaseAPIResponse(BaseModel):
    disease_name: str
    description: str
    severity: str
    treatment_recommendations: List[str]

# Respuestas del controlador
class DiagnosticResponse(BaseModel):
    id: str
    user_id: str
    username: str
    user_input: str
    symptoms: List[str]
    initial_diagnosis: str
    final_diagnosis: str
    created_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

class SymptomsResponse(BaseModel):
    id: str
    user_id: str
    username: str
    user_input: str
    symptoms: List[str]
    created_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

class ExplainDiseaseResponse(BaseModel):
    id: str
    user_id: str
    username: str
    diagnosis: str
    disease_name: str
    description: str
    severity: str
    treatment_recommendations: List[str]
    created_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

# Modelos para crear registros
class DiagnosticCreate(BaseModel):
    user_input: str
    symptoms: List[str]
    initial_diagnosis: str
    final_diagnosis: str

class SymptomsCreate(BaseModel):
    user_input: str
    symptoms: List[str]

class ExplainDiseaseCreate(BaseModel):
    diagnosis: str
    disease_name: str
    description: str
    severity: str
    treatment_recommendations: List[str]