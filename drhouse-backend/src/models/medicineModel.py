from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from enum import Enum

class MedicineMode(str, Enum):
    INFO = "info"
    SIDE_EFFECTS = "side_effects"
    USES = "uses"

class MedicineRequest(BaseModel):
    medicine_name: str
    mode: MedicineMode = Field(default=MedicineMode.INFO, description="Modalidad de consulta de medicamento")

class MedicineInfoRequest(BaseModel):
    medicine_name: str

class MedicineSideEffectsRequest(BaseModel):
    medicine_name: str

class MedicineUsesRequest(BaseModel):
    medicine_name: str

# Respuestas de la API externa
class MedicineInfoAPIResponse(BaseModel):
    medicine_name: str
    description: str
    uses: List[str]
    manufacturer: str
    availability: str
    warnings: str

class MedicineSideEffectsAPIResponse(BaseModel):
    medicine_name: str
    common_side_effects: List[str]
    serious_side_effects: List[str]
    rare_side_effects: List[str]
    warnings: str

class MedicineUsesAPIResponse(BaseModel):
    medicine_name: str
    primary_uses: List[str]
    secondary_uses: List[str]
    conditions_treated: List[str]
    dosage_info: str

# Respuestas del controlador
class MedicineInfoResponse(BaseModel):
    id: str
    user_id: Optional[str] = "anonymous"
    username: Optional[str] = "anonymous"
    medicine_name: str
    description: str
    uses: List[str]
    manufacturer: str
    availability: str
    warnings: str
    created_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

class MedicineSideEffectsResponse(BaseModel):
    id: str
    user_id: Optional[str] = "anonymous"
    username: Optional[str] = "anonymous"
    medicine_name: str
    common_side_effects: List[str]
    serious_side_effects: List[str]
    rare_side_effects: List[str]
    warnings: str
    created_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

class MedicineUsesResponse(BaseModel):
    id: str
    user_id: Optional[str] = "anonymous"
    username: Optional[str] = "anonymous"
    medicine_name: str
    primary_uses: List[str]
    secondary_uses: List[str]
    conditions_treated: List[str]
    dosage_info: str
    created_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

# Modelos para crear registros
class MedicineInfoCreate(BaseModel):
    medicine_name: str
    description: str
    uses: List[str]
    manufacturer: str
    availability: str
    warnings: str

class MedicineSideEffectsCreate(BaseModel):
    medicine_name: str
    common_side_effects: List[str]
    serious_side_effects: List[str]
    rare_side_effects: List[str]
    warnings: str

class MedicineUsesCreate(BaseModel):
    medicine_name: str
    primary_uses: List[str]
    secondary_uses: List[str]
    conditions_treated: List[str]
    dosage_info: str