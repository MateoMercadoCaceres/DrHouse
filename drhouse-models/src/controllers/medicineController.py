from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.medicineService import MedicineService
from models.medicalSchemas import (
    MedicineInfoResponse,
    SideEffectsResponse,
    MedicineUsesResponse,
    SymptomAnalysisRequest,
    MedicineRecommendationResponse
)

router = APIRouter()
medicine_service = MedicineService()

@router.get("/medicine/{medicine_name}/info", response_model=MedicineInfoResponse)
async def get_medicine_info(medicine_name: str):
    """
    Obtiene información general de un medicamento incluyendo descripción, usos, fabricante y disponibilidad.
    """
    try:
        result = await medicine_service.get_medicine_info(medicine_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener información del medicamento: {str(e)}")

@router.get("/medicine/{medicine_name}/side-effects", response_model=SideEffectsResponse)
async def get_medicine_side_effects(medicine_name: str):
    """
    Obtiene los efectos secundarios de un medicamento específico.
    """
    try:
        result = await medicine_service.get_side_effects(medicine_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener efectos secundarios: {str(e)}")

@router.get("/medicine/{medicine_name}/uses", response_model=MedicineUsesResponse)
async def get_medicine_uses(medicine_name: str):
    """
    Obtiene los usos terapéuticos de un medicamento para diferentes dolores o enfermedades.
    """
    try:
        result = await medicine_service.get_medicine_uses(medicine_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usos del medicamento: {str(e)}")

@router.post("/medicine/recommend", response_model=MedicineRecommendationResponse)
async def recommend_medicine(request: SymptomAnalysisRequest):
    """
    Analiza una lista de síntomas y recomienda medicamentos apropiados.
    IMPORTANTE: Esta es solo una herramienta informativa. Siempre consulte a un profesional médico.
    """
    try:
        result = await medicine_service.recommend_medicine_by_symptoms(request.symptoms)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar síntomas: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la API.
    """
    return {"status": "healthy", "service": "Medicine Information API"}