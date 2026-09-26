from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import List
from models.medicalSchemas import (
    MedicineInfoResponse,
    SideEffectsResponse,
    MedicineUsesResponse,
    MedicineRecommendationResponse
)
from prompt.medicalPrompt import MedicalPrompts

load_dotenv()

class MedicineService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.prompts = MedicalPrompts()

    async def _call_ai(self, prompt: str) -> str:
        """
        Método privado para realizar llamadas a la API de DeepSeek
        """
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "medicine-api.local",
                    "X-Title": "Medicine Information API",
                },
                model="deepseek/deepseek-chat:free",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente médico especializado. SIEMPRE debes responder únicamente con JSON válido, sin texto adicional, sin markdown, sin código. Solo el JSON puro."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error en llamada a AI: {str(e)}")

    def _clean_json_response(self, response: str) -> str:
        """
        Limpia la respuesta de la AI para obtener JSON válido
        """
        # Remover markdown code blocks si existen
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        
        # Remover saltos de línea y espacios extra
        response = response.strip()
        
        return response

    async def get_medicine_info(self, medicine_name: str) -> MedicineInfoResponse:
        """
        Obtiene información general de un medicamento
        """
        prompt = self.prompts.get_medicine_info_prompt(medicine_name)
        response = await self._call_ai(prompt)
        
        try:
            # Limpiar respuesta antes de parsear
            clean_response = self._clean_json_response(response)
            data = json.loads(clean_response)
            return MedicineInfoResponse(**data)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parseando respuesta: {e}")
            print(f"Respuesta original: {response}")
            # Si no es JSON válido, crear respuesta estructurada
            return MedicineInfoResponse(
                medicine_name=medicine_name,
                description=f"Error al procesar información del medicamento {medicine_name}. Respuesta recibida: {response[:200]}...",
                uses=["Error al obtener información"],
                manufacturer="No especificado",
                availability="Consulte con su farmacia local",
                warnings="Siempre consulte con un profesional médico antes de usar cualquier medicamento"
            )

    async def get_side_effects(self, medicine_name: str) -> SideEffectsResponse:
        """
        Obtiene los efectos secundarios de un medicamento
        """
        prompt = self.prompts.get_side_effects_prompt(medicine_name)
        response = await self._call_ai(prompt)
        
        try:
            clean_response = self._clean_json_response(response)
            data = json.loads(clean_response)
            return SideEffectsResponse(**data)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parseando efectos secundarios: {e}")
            print(f"Respuesta original: {response}")
            return SideEffectsResponse(
                medicine_name=medicine_name,
                common_side_effects=[f"Error al procesar información. Respuesta: {response[:100]}..."],
                serious_side_effects=["Consulte la información del fabricante"],
                rare_side_effects=[],
                warnings="Consulte con un profesional médico para información detallada sobre efectos secundarios"
            )

    async def get_medicine_uses(self, medicine_name: str) -> MedicineUsesResponse:
        """
        Obtiene los usos terapéuticos de un medicamento
        """
        prompt = self.prompts.get_medicine_uses_prompt(medicine_name)
        response = await self._call_ai(prompt)
        
        try:
            clean_response = self._clean_json_response(response)
            data = json.loads(clean_response)
            return MedicineUsesResponse(**data)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parseando usos del medicamento: {e}")
            print(f"Respuesta original: {response}")
            return MedicineUsesResponse(
                medicine_name=medicine_name,
                primary_uses=[f"Error al procesar información. Respuesta: {response[:100]}..."],
                secondary_uses=[],
                conditions_treated=[],
                dosage_info="Consulte con un profesional médico para información sobre dosificación"
            )

    async def recommend_medicine_by_symptoms(self, symptoms: List[str]) -> MedicineRecommendationResponse:
        """
        Recomienda medicamentos basado en síntomas
        """
        prompt = self.prompts.get_symptom_analysis_prompt(symptoms)
        response = await self._call_ai(prompt)
        
        try:
            clean_response = self._clean_json_response(response)
            data = json.loads(clean_response)
            return MedicineRecommendationResponse(**data)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parseando recomendaciones: {e}")
            print(f"Respuesta original: {response}")
            return MedicineRecommendationResponse(
                symptoms=symptoms,
                recommended_medicines=[f"Error al procesar recomendación. Respuesta: {response[:100]}..."],
                severity_assessment="Indeterminado",
                medical_advice="IMPORTANTE: Esta es solo información general. Consulte SIEMPRE con un profesional médico para un diagnóstico y tratamiento adecuados.",
                emergency_warning="Si experimenta síntomas graves, busque atención médica inmediata"
            )