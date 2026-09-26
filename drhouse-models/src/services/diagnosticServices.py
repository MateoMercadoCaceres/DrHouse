from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import logging
from typing import List, Dict, Any
from prompt.diagnosticPrompt import DiagnosticPrompts
from models.diagnoticSchema import SymptomsResponse, DiagnosticResponse, DiseaseExplanationResponse, SeverityLevel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiagnosticService:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.model = "deepseek/deepseek-r1-0528:free"
        self.prompts = DiagnosticPrompts()
    
    def _manual_json_parse(self, response: str) -> Dict[str, Any]:
        """
        Parseo manual para casos donde el JSON no está bien formateado
        """
        import re
        
        # Extraer síntomas
        symptoms_match = re.search(r'"symptoms"\s*:\s*\[(.*?)\]', response, re.DOTALL)
        symptoms = []
        if symptoms_match:
            symptoms_str = symptoms_match.group(1)
            # Extraer cada síntoma entre comillas
            symptom_matches = re.findall(r'"([^"]*)"', symptoms_str)
            symptoms = symptom_matches
        
        # Extraer diagnóstico inicial
        initial_diagnosis_match = re.search(r'"initial_diagnosis"\s*:\s*"([^"]*)"', response)
        initial_diagnosis = initial_diagnosis_match.group(1) if initial_diagnosis_match else "No definido"
        
        # Extraer diagnóstico final
        final_diagnosis_match = re.search(r'"final_diagnosis"\s*:\s*"([^"]*)"', response)
        final_diagnosis = final_diagnosis_match.group(1) if final_diagnosis_match else "Diagnóstico no disponible"
        
        # Extraer nombre de enfermedad (para explain_disease)
        disease_name_match = re.search(r'"disease_name"\s*:\s*"([^"]*)"', response)
        disease_name = disease_name_match.group(1) if disease_name_match else ""
        
        # Extraer descripción
        description_match = re.search(r'"description"\s*:\s*"([^"]*)"', response)
        description = description_match.group(1) if description_match else ""
        
        # Extraer severidad
        severity_match = re.search(r'"severity"\s*:\s*"([^"]*)"', response)
        severity = severity_match.group(1) if severity_match else "moderado"
        
        # Extraer recomendaciones de tratamiento
        treatment_match = re.search(r'"treatment_recommendations"\s*:\s*\[(.*?)\]', response, re.DOTALL)
        treatment_recommendations = []
        if treatment_match:
            treatment_str = treatment_match.group(1)
            treatment_matches = re.findall(r'"([^"]*)"', treatment_str)
            treatment_recommendations = treatment_matches
        
        # Determinar qué tipo de respuesta es basado en los campos presentes
        if disease_name and description:
            return {
                "disease_name": disease_name,
                "description": description,
                "severity": severity,
                "treatment_recommendations": treatment_recommendations
            }
        elif initial_diagnosis:
            return {
                "symptoms": symptoms,
                "initial_diagnosis": initial_diagnosis,
                "final_diagnosis": final_diagnosis
            }
        else:
            return {
                "symptoms": symptoms
            }

    async def _make_api_call(self, prompt: str) -> str:
        """
        Realiza una llamada a la API de DeepSeek
        """
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "diagnostic-api",
                    "X-Title": "Diagnostic Medical API",
                },
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente médico profesional y especializado. IMPORTANTE: Responde ÚNICAMENTE con JSON válido, sin usar \\boxed{}, sin markdown, sin texto adicional. Solo el JSON puro."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Mayor consistencia
                max_tokens=1500,
                stop=None
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error en la llamada a la API: {str(e)}")
            raise Exception(f"Error al procesar la solicitud: {str(e)}")
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parsea la respuesta JSON de la API
        """
        try:
            # Limpiar la respuesta para extraer solo el JSON
            response = response.strip()
            
            # Remover bloques de código markdown
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            elif response.startswith("```"):
                response = response.replace("```", "").strip()
            
            # Remover formato LaTeX \boxed{}
            if response.startswith("\\boxed{") and response.endswith("}"):
                response = response[7:-1].strip()  # Remover \boxed{ y }
            
            # Remover saltos de línea y espacios extra
            response = response.replace("\n", " ").strip()
            
            # Si aún hay problemas, intentar extraer JSON entre llaves
            if not response.startswith("{"):
                # Buscar el primer { y el último }
                start_idx = response.find("{")
                end_idx = response.rfind("}")
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    response = response[start_idx:end_idx + 1]
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {str(e)}, Respuesta original: {response}")
            # Intentar parseo manual como último recurso
            try:
                return self._manual_json_parse(response)
            except:
                raise Exception("Error al procesar la respuesta de la API")
    
    async def extract_symptoms(self, user_input: str) -> SymptomsResponse:
        """
        Extrae síntomas de la descripción del usuario
        """
        try:
            prompt = self.prompts.get_symptoms_extraction_prompt(user_input)
            response = await self._make_api_call(prompt)
            parsed_response = self._parse_json_response(response)
            
            return SymptomsResponse(
                symptoms=parsed_response.get("symptoms", []),
                user_input=user_input
            )
        except Exception as e:
            logger.error(f"Error en extract_symptoms: {str(e)}")
            raise Exception(f"Error al extraer síntomas: {str(e)}")
    
    async def get_full_diagnosis(self, user_input: str) -> DiagnosticResponse:
        """
        Obtiene diagnóstico completo con síntomas y diagnóstico final
        """
        try:
            prompt = self.prompts.get_full_diagnostic_prompt(user_input)
            response = await self._make_api_call(prompt)
            parsed_response = self._parse_json_response(response)
            
            return DiagnosticResponse(
                symptoms=parsed_response.get("symptoms", []),
                initial_diagnosis=parsed_response.get("initial_diagnosis", "No definido"),
                final_diagnosis=parsed_response.get("final_diagnosis", "Diagnóstico no disponible"),
                user_input=user_input
            )
        except Exception as e:
            logger.error(f"Error en get_full_diagnosis: {str(e)}")
            raise Exception(f"Error al obtener diagnóstico: {str(e)}")
    
    async def explain_disease(self, diagnosis: str) -> DiseaseExplanationResponse:
        """
        Explica una enfermedad específica
        """
        try:
            prompt = self.prompts.get_disease_explanation_prompt(diagnosis)
            response = await self._make_api_call(prompt)
            parsed_response = self._parse_json_response(response)
            
            # Validar nivel de gravedad
            severity = parsed_response.get("severity", "moderado").lower()
            if severity not in [level.value for level in SeverityLevel]:
                severity = "moderado"
            
            return DiseaseExplanationResponse(
                disease_name=parsed_response.get("disease_name", diagnosis),
                description=parsed_response.get("description", "Descripción no disponible"),
                severity=SeverityLevel(severity),
                treatment_recommendations=parsed_response.get("treatment_recommendations", [])
            )
        except Exception as e:
            logger.error(f"Error en explain_disease: {str(e)}")
            raise Exception(f"Error al explicar la enfermedad: {str(e)}")
    
    def get_api_info(self) -> Dict[str, Any]:
        """
        Retorna información sobre la API
        """
        return {
            "name": "API de Diagnóstico Médico",
            "version": "1.0.0",
            "description": "API para diagnóstico médico automatizado usando DeepSeek AI. Permite extraer síntomas, realizar diagnósticos y explicar enfermedades.",
            "endpoints": [
                "GET /api/v1/info - Información de la API",
                "POST /api/v1/diagnose - Diagnóstico completo",
                "POST /api/v1/symptoms - Extracción de síntomas",
                "POST /api/v1/explain-disease - Explicación de enfermedad"
            ],
            "powered_by": "DeepSeek AI via OpenRouter"
        }