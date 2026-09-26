class DiagnosticPrompts:
    """
    Clase que contiene prompts de ingeniería para diferentes tipos de diagnóstico médico
    """
    
    @staticmethod
    def get_symptoms_extraction_prompt(user_input: str) -> str:
        """
        Prompt para extraer síntomas de la descripción del usuario
        """
        return f"""
Eres un asistente médico especializado en la identificación de síntomas. Tu tarea es analizar la descripción de un paciente y extraer ÚNICAMENTE los síntomas mencionados.

INSTRUCCIONES ESPECÍFICAS:
1. Identifica SOLO los síntomas explícitamente mencionados
2. No agregues síntomas que no estén claramente descritos
3. Usa terminología médica apropiada pero comprensible
4. Separa cada síntoma claramente
5. No incluyas diagnósticos ni especulaciones

DESCRIPCIÓN DEL PACIENTE:
"{user_input}"

FORMATO DE RESPUESTA REQUERIDO:
Responde ÚNICAMENTE con un JSON válido sin formato adicional, sin \boxed{{}}, sin código markdown, solo el JSON puro:

{{"symptoms": ["síntoma1", "síntoma2", "síntoma3"]}}

EJEMPLO:
Para "Me duele la cabeza y tengo fiebre", responde exactamente:
{{"symptoms": ["dolor de cabeza", "fiebre"]}}

IMPORTANTE: Responde SOLO con el JSON, sin texto adicional, sin \boxed{{}}, sin markdown.
"""

    @staticmethod
    def get_full_diagnostic_prompt(user_input: str) -> str:
        """
        Prompt para diagnóstico completo con síntomas y diagnóstico final
        """
        return f"""
Eres un médico especialista con amplia experiencia en diagnóstico clínico. Analiza la descripción del paciente y proporciona un diagnóstico estructurado.

DESCRIPCIÓN DEL PACIENTE:
"{user_input}"

INSTRUCCIONES PARA EL DIAGNÓSTICO:
1. SÍNTOMAS: Identifica todos los síntomas mencionados explícitamente
2. DIAGNÓSTICO INICIAL: Siempre responde "No definido" (según especificaciones)
3. DIAGNÓSTICO FINAL: Basándote en los síntomas, proporciona el diagnóstico más probable

CONSIDERACIONES IMPORTANTES:
- Usa terminología médica precisa pero comprensible
- Considera la combinación de síntomas para el diagnóstico
- Si hay múltiples posibilidades, elige la más probable
- Se conservador en el diagnóstico si la información es limitada

FORMATO DE RESPUESTA REQUERIDO:
Responde ÚNICAMENTE con un JSON válido sin formato adicional, sin \boxed{{}}, sin código markdown, solo el JSON puro:

{{"symptoms": ["síntoma1", "síntoma2"], "initial_diagnosis": "No definido", "final_diagnosis": "diagnóstico_más_probable"}}

EJEMPLO:
Para "Tengo dolor de cabeza intenso, náuseas y sensibilidad a la luz", responde exactamente:
{{"symptoms": ["dolor de cabeza intenso", "náuseas", "fotofobia"], "initial_diagnosis": "No definido", "final_diagnosis": "migraña"}}

IMPORTANTE: Responde SOLO con el JSON, sin texto adicional, sin \boxed{{}}, sin markdown.
"""

    @staticmethod
    def get_disease_explanation_prompt(diagnosis: str) -> str:
        """
        Prompt para explicar una enfermedad específica
        """
        return f"""
Eres un médico especialista educador. Tu tarea es explicar la enfermedad "{diagnosis}" de manera clara y completa para un paciente.

ENFERMEDAD A EXPLICAR: {diagnosis}

INSTRUCCIONES PARA LA EXPLICACIÓN:
1. DESCRIPCIÓN: Explica qué es la enfermedad de manera clara y comprensible
2. GRAVEDAD: Evalúa el nivel de gravedad (leve, moderado, grave, crítico)
3. RECOMENDACIONES: Proporciona recomendaciones generales de tratamiento

CRITERIOS PARA GRAVEDAD:
- LEVE: Síntomas manejables, no requiere atención médica inmediata
- MODERADO: Síntomas que requieren seguimiento médico
- GRAVE: Requiere atención médica pronta
- CRÍTICO: Requiere atención médica inmediata/urgente

FORMATO DE RESPUESTA REQUERIDO:
Responde ÚNICAMENTE con un JSON válido sin formato adicional, sin \boxed{{}}, sin código markdown, solo el JSON puro:

{{"disease_name": "{diagnosis}", "description": "explicación_detallada", "severity": "nivel_gravedad", "treatment_recommendations": ["rec1", "rec2", "rec3"]}}

EJEMPLO:
Para "migraña", responde exactamente:
{{"disease_name": "migraña", "description": "La migraña es un tipo de dolor de cabeza recurrente que puede ser de intensidad moderada a severa", "severity": "moderado", "treatment_recommendations": ["Descansar en lugar oscuro", "Aplicar compresas frías", "Consultar médico"]}}

IMPORTANTE: 
- Responde SOLO con el JSON, sin texto adicional, sin \boxed{{}}, sin markdown
- Usa solo estos valores para severity: leve, moderado, grave, crítico
- Proporciona información médica general, NO reemplaza consulta médica profesional
"""