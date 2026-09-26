from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.diagnoticSchema import (
    UserInputRequest, 
    DiagnosisRequest, 
    SymptomsResponse, 
    DiagnosticResponse, 
    DiseaseExplanationResponse, 
    APIInfoResponse,
    ErrorResponse
)
from services.diagnosticServices import DiagnosticService
import logging

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()
diagnostic_service = DiagnosticService()

@router.get(
    "/info",
    response_model=APIInfoResponse,
    summary="Información de la API",
    description="Obtiene información general sobre la API de diagnóstico médico"
)
async def get_api_info():
    """
    Endpoint para obtener información general de la API
    """
    try:
        info = diagnostic_service.get_api_info()
        return APIInfoResponse(**info)
    except Exception as e:
        logger.error(f"Error en get_api_info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post(
    "/diagnose",
    response_model=DiagnosticResponse,
    summary="Diagnóstico médico completo",
    description="Realiza un diagnóstico médico completo basado en la descripción de síntomas del usuario. Retorna síntomas identificados, diagnóstico inicial y diagnóstico final.",
    responses={
        200: {
            "description": "Diagnóstico realizado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "symptoms": ["dolor de cabeza intenso", "náuseas", "fotofobia"],
                        "initial_diagnosis": "No definido",
                        "final_diagnosis": "migraña",
                        "user_input": "Me duele mucho la cabeza y tengo náuseas"
                    }
                }
            }
        },
        400: {"model": ErrorResponse, "description": "Solicitud inválida"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def diagnose_symptoms(request: UserInputRequest):
    """
    Endpoint para realizar diagnóstico médico completo
    
    - **user_input**: Descripción de los síntomas en lenguaje natural
    
    Retorna:
    - Lista de síntomas identificados
    - Diagnóstico inicial (siempre "No definido")
    - Diagnóstico final basado en los síntomas
    """
    try:
        if not request.user_input.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La descripción de síntomas no puede estar vacía"
            )
        
        result = await diagnostic_service.get_full_diagnosis(request.user_input)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en diagnose_symptoms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el diagnóstico: {str(e)}"
        )

@router.post(
    "/symptoms",
    response_model=SymptomsResponse,
    summary="Extracción de síntomas",
    description="Extrae y lista los síntomas mencionados en la descripción del usuario",
    responses={
        200: {
            "description": "Síntomas extraídos exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "symptoms": ["dolor de cabeza", "fiebre alta"],
                        "user_input": "Me duele mucho la cabeza y tengo fiebre alta desde ayer"
                    }
                }
            }
        },
        400: {"model": ErrorResponse, "description": "Solicitud inválida"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def extract_symptoms(request: UserInputRequest):
    """
    Endpoint para extraer síntomas de la descripción del usuario
    
    - **user_input**: Descripción de los síntomas en lenguaje natural
    
    Retorna:
    - Lista de síntomas identificados
    - Entrada original del usuario
    """
    try:
        if not request.user_input.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La descripción de síntomas no puede estar vacía"
            )
        
        result = await diagnostic_service.extract_symptoms(request.user_input)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en extract_symptoms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al extraer síntomas: {str(e)}"
        )

@router.post(
    "/explain-disease",
    response_model=DiseaseExplanationResponse,
    summary="Explicación de enfermedad",
    description="Proporciona una explicación detallada de una enfermedad específica, incluyendo descripción, gravedad y recomendaciones de tratamiento",
    responses={
        200: {
            "description": "Explicación de enfermedad generada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "disease_name": "migraña",
                        "description": "La migraña es un tipo de dolor de cabeza recurrente...",
                        "severity": "moderado",
                        "treatment_recommendations": [
                            "Descansar en un lugar oscuro y silencioso",
                            "Aplicar compresas frías en la frente",
                            "Consultar con un médico para medicamentos específicos"
                        ]
                    }
                }
            }
        },
        400: {"model": ErrorResponse, "description": "Solicitud inválida"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def explain_disease(request: DiagnosisRequest):
    """
    Endpoint para explicar una enfermedad específica
    
    - **diagnosis**: Nombre de la enfermedad o diagnóstico a explicar
    
    Retorna:
    - Nombre de la enfermedad
    - Descripción detallada
    - Nivel de gravedad
    - Recomendaciones de tratamiento
    """
    try:
        if not request.diagnosis.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la enfermedad no puede estar vacío"
            )
        
        result = await diagnostic_service.explain_disease(request.diagnosis)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en explain_disease: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al explicar la enfermedad: {str(e)}"
        )