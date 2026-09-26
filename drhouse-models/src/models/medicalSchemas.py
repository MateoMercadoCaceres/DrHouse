from pydantic import BaseModel, Field
from typing import List, Optional

class MedicineInfoResponse(BaseModel):
    """
    Esquema para la respuesta de información general de medicamentos
    """
    medicine_name: str = Field(..., description="Nombre del medicamento")
    description: str = Field(..., description="Descripción general del medicamento")
    uses: List[str] = Field(..., description="Lista de usos principales del medicamento")
    manufacturer: str = Field(..., description="Fabricante del medicamento")
    availability: str = Field(..., description="Información sobre dónde conseguir el medicamento")
    warnings: str = Field(..., description="Advertencias importantes sobre el uso")

class SideEffectsResponse(BaseModel):
    """
    Esquema para la respuesta de efectos secundarios
    """
    medicine_name: str = Field(..., description="Nombre del medicamento")
    common_side_effects: List[str] = Field(..., description="Efectos secundarios comunes")
    serious_side_effects: List[str] = Field(..., description="Efectos secundarios graves")
    rare_side_effects: List[str] = Field(default=[], description="Efectos secundarios raros")
    warnings: str = Field(..., description="Advertencias sobre efectos secundarios")

class MedicineUsesResponse(BaseModel):
    """
    Esquema para la respuesta de usos de medicamentos
    """
    medicine_name: str = Field(..., description="Nombre del medicamento")
    primary_uses: List[str] = Field(..., description="Usos primarios del medicamento")
    secondary_uses: List[str] = Field(default=[], description="Usos secundarios del medicamento")
    conditions_treated: List[str] = Field(default=[], description="Condiciones médicas que trata")
    dosage_info: str = Field(..., description="Información general sobre dosificación")

class SymptomAnalysisRequest(BaseModel):
    """
    Esquema para la solicitud de análisis de síntomas
    """
    symptoms: List[str] = Field(..., min_items=1, description="Lista de síntomas a analizar")

class MedicineRecommendationResponse(BaseModel):
    """
    Esquema para la respuesta de recomendación de medicamentos
    """
    symptoms: List[str] = Field(..., description="Síntomas analizados")
    recommended_medicines: List[str] = Field(..., description="Medicamentos recomendados")
    severity_assessment: str = Field(..., description="Evaluación de la gravedad de los síntomas")
    medical_advice: str = Field(..., description="Consejo médico general")
    emergency_warning: str = Field(..., description="Advertencia sobre situaciones de emergencia")

class ErrorResponse(BaseModel):
    """
    Esquema para respuestas de error
    """
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    
class HealthResponse(BaseModel):
    """
    Esquema para el endpoint de health check
    """
    status: str = Field(..., description="Estado del servicio")
    service: str = Field(..., description="Nombre del servicio")