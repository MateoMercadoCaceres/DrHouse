from dotenv import load_dotenv
import os
import json
import logging
import httpx
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pymongo.database import Database
from repositories.diagnosticRepository import DiagnosticRepository
from models.diagnosticModel import (
    DiagnosticResponse, 
    SymptomsResponse, 
    ExplainDiseaseResponse,
    DiagnosticAPIResponse,
    SymptomsAPIResponse,
    ExplainDiseaseAPIResponse
)
from models.diagnoticSchema import SeverityLevel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiagnosticService:
    def __init__(self, db: Database):
        load_dotenv()
        self.base_url = os.getenv("DIAGNOSTIC_API_BASE_URL")
        if not self.base_url:
            raise ValueError("DIAGNOSTIC_API_BASE_URL no está configurada en el archivo .env")
        self.repository = DiagnosticRepository(db)
    
    async def _make_api_call(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza una llamada a la API de diagnóstico
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/{endpoint}",
                    json=data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error en la llamada a la API: {str(e)}")
            raise Exception(f"Error al procesar la solicitud: {str(e)}")

    # Métodos para llamadas a la API externa
    async def _extract_symptoms_api(self, user_input: str) -> SymptomsAPIResponse:
        """Extrae síntomas usando la API externa"""
        try:
            response = await self._make_api_call("symptoms", {"user_input": user_input})
            return SymptomsAPIResponse(
                symptoms=response.get("symptoms", []),
                user_input=user_input
            )
        except Exception as e:
            logger.error(f"Error en _extract_symptoms_api: {str(e)}")
            raise Exception(f"Error al extraer síntomas: {str(e)}")

    async def _get_full_diagnosis_api(self, user_input: str) -> DiagnosticAPIResponse:
        """Obtiene diagnóstico completo usando la API externa"""
        try:
            response = await self._make_api_call("diagnose", {"user_input": user_input})
            return DiagnosticAPIResponse(
                symptoms=response.get("symptoms", []),
                initial_diagnosis=response.get("initial_diagnosis", "No definido"),
                final_diagnosis=response.get("final_diagnosis", "Diagnóstico no disponible"),
                user_input=user_input
            )
        except Exception as e:
            logger.error(f"Error en _get_full_diagnosis_api: {str(e)}")
            raise Exception(f"Error al obtener diagnóstico: {str(e)}")

    async def _explain_disease_api(self, diagnosis: str) -> ExplainDiseaseAPIResponse:
        """Explica una enfermedad usando la API externa"""
        try:
            response = await self._make_api_call("explain-disease", {"diagnosis": diagnosis})
            
            severity = response.get("severity", "moderado").lower()
            if severity not in [level.value for level in SeverityLevel]:
                severity = "moderado"
            
            return ExplainDiseaseAPIResponse(
                disease_name=response.get("disease_name", diagnosis),
                description=response.get("description", "Descripción no disponible"),
                severity=severity,
                treatment_recommendations=response.get("treatment_recommendations", [])
            )
        except Exception as e:
            logger.error(f"Error en _explain_disease_api: {str(e)}")
            raise Exception(f"Error al explicar la enfermedad: {str(e)}")

    # Métodos principales del servicio
    async def create_diagnostic(self, user_input: str, current_user: Dict[str, Any]) -> DiagnosticResponse:
        """Crea un diagnóstico completo"""
        try:
            # Llamar a la API externa
            api_response = await self._get_full_diagnosis_api(user_input)
            
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            # Preparar datos para guardar
            diagnostic_data = {
                "user_id": user_id,
                "username": current_user["username"],
                "user_input": user_input,
                "symptoms": api_response.symptoms,
                "initial_diagnosis": api_response.initial_diagnosis,
                "final_diagnosis": api_response.final_diagnosis,
                "mode": "diagnose",
                "created_at": datetime.utcnow()
            }
            
            # Guardar en base de datos
            diagnostic_id = await self.repository.create_diagnostic(diagnostic_data)
            if not diagnostic_id:
                raise Exception("Error al guardar el diagnóstico")
            
            return DiagnosticResponse(
                id=diagnostic_id,
                user_id=user_id,
                username=current_user["username"],
                user_input=user_input,
                symptoms=api_response.symptoms,
                initial_diagnosis=api_response.initial_diagnosis,
                final_diagnosis=api_response.final_diagnosis,
                created_at=diagnostic_data["created_at"]
            )
            
        except Exception as e:
            logger.error(f"Error en create_diagnostic: {str(e)}")
            raise Exception(f"Error al crear diagnóstico: {str(e)}")

    async def create_symptoms_extraction(self, user_input: str, current_user: Dict[str, Any]) -> SymptomsResponse:
        """Crea una extracción de síntomas"""
        try:
            # Llamar a la API externa
            api_response = await self._extract_symptoms_api(user_input)
            
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            # Preparar datos para guardar
            symptoms_data = {
                "user_id": user_id,
                "username": current_user["username"],
                "user_input": user_input,
                "symptoms": api_response.symptoms,
                "mode": "symptoms",
                "created_at": datetime.utcnow()
            }
            
            # Guardar en base de datos
            symptoms_id = await self.repository.create_symptoms(symptoms_data)
            if not symptoms_id:
                raise Exception("Error al guardar la extracción de síntomas")
            
            return SymptomsResponse(
                id=symptoms_id,
                user_id=user_id,
                username=current_user["username"],
                user_input=user_input,
                symptoms=api_response.symptoms,
                created_at=symptoms_data["created_at"]
            )
            
        except Exception as e:
            logger.error(f"Error en create_symptoms_extraction: {str(e)}")
            raise Exception(f"Error al extraer síntomas: {str(e)}")

    async def create_disease_explanation(self, diagnosis: str, current_user: Dict[str, Any]) -> ExplainDiseaseResponse:
        """Crea una explicación de enfermedad"""
        try:
            # Llamar a la API externa
            api_response = await self._explain_disease_api(diagnosis)
            
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            # Preparar datos para guardar
            explanation_data = {
                "user_id": user_id,
                "username": current_user["username"],
                "diagnosis": diagnosis,
                "disease_name": api_response.disease_name,
                "description": api_response.description,
                "severity": api_response.severity,
                "treatment_recommendations": api_response.treatment_recommendations,
                "mode": "explain",
                "created_at": datetime.utcnow()
            }
            
            # Guardar en base de datos
            explanation_id = await self.repository.create_disease_explanation(explanation_data)
            if not explanation_id:
                raise Exception("Error al guardar la explicación de enfermedad")
            
            return ExplainDiseaseResponse(
                id=explanation_id,
                user_id=user_id,
                username=current_user["username"],
                diagnosis=diagnosis,
                disease_name=api_response.disease_name,
                description=api_response.description,
                severity=api_response.severity,
                treatment_recommendations=api_response.treatment_recommendations,
                created_at=explanation_data["created_at"]
            )
            
        except Exception as e:
            logger.error(f"Error en create_disease_explanation: {str(e)}")
            raise Exception(f"Error al explicar enfermedad: {str(e)}")

    async def get_user_diagnostics(self, current_user: Dict[str, Any], limit: int = 20, skip: int = 0, mode: Optional[str] = None) -> List[Union[DiagnosticResponse, SymptomsResponse, ExplainDiseaseResponse]]:
        """Obtiene todos los diagnósticos del usuario con filtro opcional por modo"""
        try:
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            diagnostics = await self.repository.get_diagnostics_by_user_id(user_id, limit, skip, mode)
            
            result = []
            for diagnostic in diagnostics:
                diagnostic_mode = diagnostic.get("mode", "diagnose")
                
                if diagnostic_mode == "symptoms":
                    result.append(SymptomsResponse(
                        id=diagnostic["_id"],
                        user_id=diagnostic["user_id"],
                        username=diagnostic["username"],
                        user_input=diagnostic["user_input"],
                        symptoms=diagnostic["symptoms"],
                        created_at=diagnostic["created_at"]
                    ))
                elif diagnostic_mode == "explain":
                    result.append(ExplainDiseaseResponse(
                        id=diagnostic["_id"],
                        user_id=diagnostic["user_id"],
                        username=diagnostic["username"],
                        diagnosis=diagnostic["diagnosis"],
                        disease_name=diagnostic["disease_name"],
                        description=diagnostic["description"],
                        severity=diagnostic["severity"],
                        treatment_recommendations=diagnostic["treatment_recommendations"],
                        created_at=diagnostic["created_at"]
                    ))
                else:  # diagnose
                    result.append(DiagnosticResponse(
                        id=diagnostic["_id"],
                        user_id=diagnostic["user_id"],
                        username=diagnostic["username"],
                        user_input=diagnostic["user_input"],
                        symptoms=diagnostic["symptoms"],
                        initial_diagnosis=diagnostic["initial_diagnosis"],
                        final_diagnosis=diagnostic["final_diagnosis"],
                        created_at=diagnostic["created_at"]
                    ))
            
            return result
            
        except Exception as e:
            logger.error(f"Error en get_user_diagnostics: {str(e)}")
            raise Exception(f"Error al obtener diagnósticos: {str(e)}")

    async def count_user_diagnostics(self, current_user: Dict[str, Any], mode: Optional[str] = None) -> int:
        """Cuenta diagnósticos del usuario con filtro opcional por modo"""
        try:
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            return await self.repository.count_diagnostics_by_user_id(user_id, mode)
        except Exception as e:
            logger.error(f"Error en count_user_diagnostics: {str(e)}")
            raise Exception(f"Error al contar diagnósticos: {str(e)}")

    async def get_diagnostic_by_id(self, diagnostic_id: str, current_user: Dict[str, Any]) -> Optional[Union[DiagnosticResponse, SymptomsResponse, ExplainDiseaseResponse]]:
        """Obtiene un diagnóstico específico por ID"""
        try:
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            diagnostic = await self.repository.get_diagnostic_by_id(diagnostic_id)
            
            if not diagnostic or diagnostic["user_id"] != user_id:
                return None
            
            diagnostic_mode = diagnostic.get("mode", "diagnose")
            
            if diagnostic_mode == "symptoms":
                return SymptomsResponse(
                    id=diagnostic["_id"],
                    user_id=diagnostic["user_id"],
                    username=diagnostic["username"],
                    user_input=diagnostic["user_input"],
                    symptoms=diagnostic["symptoms"],
                    created_at=diagnostic["created_at"]
                )
            elif diagnostic_mode == "explain":
                return ExplainDiseaseResponse(
                    id=diagnostic["_id"],
                    user_id=diagnostic["user_id"],
                    username=diagnostic["username"],
                    diagnosis=diagnostic["diagnosis"],
                    disease_name=diagnostic["disease_name"],
                    description=diagnostic["description"],
                    severity=diagnostic["severity"],
                    treatment_recommendations=diagnostic["treatment_recommendations"],
                    created_at=diagnostic["created_at"]
                )
            else:  # diagnose
                return DiagnosticResponse(
                    id=diagnostic["_id"],
                    user_id=diagnostic["user_id"],
                    username=diagnostic["username"],
                    user_input=diagnostic["user_input"],
                    symptoms=diagnostic["symptoms"],
                    initial_diagnosis=diagnostic["initial_diagnosis"],
                    final_diagnosis=diagnostic["final_diagnosis"],
                    created_at=diagnostic["created_at"]
                )
                
        except Exception as e:
            logger.error(f"Error en get_diagnostic_by_id: {str(e)}")
            raise Exception(f"Error al obtener diagnóstico: {str(e)}")

    async def delete_diagnostic(self, diagnostic_id: str, current_user: Dict[str, Any]) -> bool:
        """Elimina un diagnóstico específico"""
        try:
            # Obtener el ID del usuario (puede ser _id o id)
            user_id = current_user.get("_id") or current_user.get("id")
            if not user_id:
                raise Exception("No se pudo obtener el ID del usuario")
            
            return await self.repository.delete_diagnostic(diagnostic_id, user_id)
        except Exception as e:
            logger.error(f"Error en delete_diagnostic: {str(e)}")
            raise Exception(f"Error al eliminar diagnóstico: {str(e)}")

    def get_api_info(self) -> Dict[str, Any]:
        """Retorna información sobre la API"""
        return {
            "name": "API de Diagnóstico Médico",
            "version": "2.0.0",
            "description": "API para diagnóstico médico automatizado. Soporta múltiples modalidades: diagnóstico completo, extracción de síntomas y explicación de enfermedades.",
            "endpoints": [
                "POST /api/diagnostics - Diagnóstico según modalidad (mode: diagnose, symptoms, explain)",
                "POST /api/diagnostics/symptoms - Extracción de síntomas",
                "POST /api/diagnostics/explain-disease - Explicación de enfermedad",
                "GET /api/diagnostics - Obtener diagnósticos del usuario",
                "GET /api/diagnostics/count - Contar diagnósticos del usuario",
                "GET /api/diagnostics/{id} - Obtener diagnóstico específico",
                "DELETE /api/diagnostics/{id} - Eliminar diagnóstico"
            ],
            "modes": {
                "diagnose": "Diagnóstico médico completo con síntomas y diagnósticos inicial/final",
                "symptoms": "Extracción de síntomas desde descripción del usuario",
                "explain": "Explicación detallada de una enfermedad o diagnóstico"
            },
            "powered_by": "API de Diagnóstico Médico Externa"
        }