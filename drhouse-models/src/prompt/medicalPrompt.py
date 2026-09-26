from typing import List

class MedicalPrompts:
    """
    Clase que contiene todos los prompts para consultas médicas
    """
    
    def get_medicine_info_prompt(self, medicine_name: str) -> str:
        """
        Prompt para obtener información general de un medicamento
        """
        return f"""
Proporciona información sobre el medicamento '{medicine_name}' en formato JSON exacto.

Responde ÚNICAMENTE con este JSON (sin markdown, sin texto adicional):

{{
    "medicine_name": "{medicine_name}",
    "description": "[Descripción detallada del medicamento, composición y mecanismo de acción]",
    "uses": ["[uso principal 1]", "[uso principal 2]", "[uso principal 3]"],
    "manufacturer": "[Fabricante principal o 'Múltiples fabricantes']",
    "availability": "[Con receta médica/Sin receta/Información de disponibilidad]",
    "warnings": "[Advertencias importantes sobre el uso]"
}}

CRÍTICO: Responde solo con JSON válido, sin bloques de código, sin explicaciones adicionales.
        """

    def get_side_effects_prompt(self, medicine_name: str) -> str:
        """
        Prompt para obtener efectos secundarios de un medicamento
        """
        return f"""
Proporciona efectos secundarios del medicamento '{medicine_name}' en formato JSON exacto.

Responde ÚNICAMENTE con este JSON (sin markdown, sin texto adicional):

{{
    "medicine_name": "{medicine_name}",
    "common_side_effects": ["[efecto común 1]", "[efecto común 2]", "[efecto común 3]"],
    "serious_side_effects": ["[efecto grave 1]", "[efecto grave 2]"],
    "rare_side_effects": ["[efecto raro 1]", "[efecto raro 2]"],
    "warnings": "[Cuándo contactar médico y advertencias importantes]"
}}

CRÍTICO: Responde solo con JSON válido, sin bloques de código, sin explicaciones adicionales.
        """

    def get_medicine_uses_prompt(self, medicine_name: str) -> str:
        """
        Prompt para obtener usos terapéuticos de un medicamento
        """
        return f"""
Proporciona usos terapéuticos del medicamento '{medicine_name}' en formato JSON exacto.

Responde ÚNICAMENTE con este JSON (sin markdown, sin texto adicional):

{{
    "medicine_name": "{medicine_name}",
    "primary_uses": ["[uso principal 1]", "[uso principal 2]"],
    "secondary_uses": ["[uso secundario 1]", "[uso secundario 2]"],
    "conditions_treated": ["[condición 1]", "[condición 2]", "[condición 3]"],
    "dosage_info": "[Información general sobre dosificación y administración]"
}}

CRÍTICO: Responde solo con JSON válido, sin bloques de código, sin explicaciones adicionales.
        """

    def get_symptom_analysis_prompt(self, symptoms: List[str]) -> str:
        """
        Prompt para analizar síntomas y recomendar medicamentos
        """
        symptoms_str = ", ".join(symptoms)
        
        return f"""
Analiza estos síntomas y proporciona recomendaciones en formato JSON exacto: {symptoms_str}

Responde ÚNICAMENTE con este JSON (sin markdown, sin texto adicional):

{{
    "symptoms": {symptoms},
    "recommended_medicines": ["[medicamento 1]", "[medicamento 2]", "[medicamento 3]"],
    "severity_assessment": "[Leve/Moderado/Grave - descripción]",
    "medical_advice": "[Consejo médico general sobre tratamiento]",
    "emergency_warning": "[Cuándo buscar atención médica inmediata]"
}}

CRÍTICO: Responde solo con JSON válido, sin bloques de código, sin explicaciones adicionales.
Recomienda solo medicamentos de venta libre apropiados.
        """

    def get_general_medical_advice_prompt(self) -> str:
        """
        Prompt para consejos médicos generales
        """
        return """
        IMPORTANTE: Todos los consejos y recomendaciones proporcionadas son solo para fines informativos 
        y no reemplazan la consulta con un profesional médico calificado.

        Principios a seguir:
        1. Nunca proporcionar diagnósticos definitivos
        2. Siempre recomendar consulta médica para síntomas graves
        3. Enfocarse en medicamentos de venta libre cuando sea apropiado
        4. Incluir advertencias de seguridad relevantes
        5. Mantener un enfoque conservador y responsable
        """