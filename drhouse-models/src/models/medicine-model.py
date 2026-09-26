import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
 
# Configuración
OUTPUT_DIR = "./medicine-gpt2-drhouse"
CSV_FILE = "../database/Medicine_Details-1 -by MaxAI.csv"  # Tu archivo CSV
 
def load_trained_model(model_path=OUTPUT_DIR, csv_file_path=CSV_FILE):
    """Carga el modelo ya entrenado"""
    print("Cargando modelo entrenado...")
    # Cargar tokenizer y modelo
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    # Mover a GPU si está disponible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    # Cargar datos de medicamentos para respuestas directas
    medicine_data = {}
    df = pd.read_csv(csv_file_path).fillna("")
    for _, row in df.iterrows():
        name = str(row['Medicine Name']).strip()
        medicine_data[name.lower()] = {
            'composition': str(row['Composition']).strip(),
            'uses': str(row['Uses']).strip(),
            'side_effects': str(row['Side_effects']).strip(),
            'manufacturer': str(row['Manufacturer']).strip()
        }
    print(f"Modelo cargado en {device}")
    print(f"Medicamentos en base de datos: {len(medicine_data)}")
    return tokenizer, model, medicine_data, device
 
def find_medicine_name(question, medicine_data):
    """Encuentra el nombre del medicamento en la pregunta"""
    q = question.lower()
    # Búsqueda exacta primero
    for name in medicine_data.keys():
        if name in q:
            return name
    # Búsqueda por palabras clave
    for name in medicine_data.keys():
        if any(len(w) > 3 and w in q for w in name.split()):
            return name
    return None
 
def get_direct_answer(question, medicine_data):
    """Obtiene respuesta directa de la base de datos"""
    q = question.lower()
    name = find_medicine_name(q, medicine_data)
    if not name:
        return None
    data = medicine_data[name]
    if 'composition' in q or 'composición' in q:
        return data['composition']
    elif 'uses' in q or 'usos' in q or 'used for' in q:
        return data['uses']
    elif 'side effect' in q or 'efectos secundarios' in q:
        return data['side_effects']
    elif 'manufacturer' in q or 'fabricante' in q:
        return data['manufacturer']
    return None
 
def generate_response(question, tokenizer, model, medicine_data, device, max_new_tokens=100):
    """Genera respuesta usando el modelo entrenado"""
    # Intentar respuesta directa primero
    direct = get_direct_answer(question, medicine_data)
    if direct and direct.strip():
        return direct, "direct"
    # Usar el modelo para generar respuesta
    prompt = f"<question>{question}<answer>"
    inputs = tokenizer(prompt, return_tensors='pt').to(device)
    with torch.no_grad():
        outputs = model.generate(
            inputs['input_ids'],
            max_new_tokens=max_new_tokens,
            temperature=0.3,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.convert_tokens_to_ids('<end>'),
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    if '<answer>' in response:
        answer = response.split('<answer>', 1)[1].split('<end>')[0]
        return answer.strip(), "generated"
    return "No pude encontrar información sobre ese medicamento.", "error"
 
def test_medicine_model():
    """Función principal para testing del modelo"""
    # Cargar modelo
    tokenizer, model, medicine_data, device = load_trained_model()
    # Ejemplos de preguntas variadas
    test_questions = [
        # Preguntas sobre composición
        "composition Efnocar 20 Tablet",
        "what is the composition of Augmentin 625 Duo Tablet",
        "composición Azithral 500 Tablet",
        # Preguntas sobre usos
        "uses Efnocar 20 Tablet",
        "what is Aciloc 150 Tablet used for",
        "para qué sirve Allegra 120mg Tablet",
        # Preguntas sobre efectos secundarios
        "side effects Efnocar 20 Tablet",
        "efectos secundarios Aricep 5 Tablet",
        "what are the side effects of Amoxyclav 625 Tablet",
        # Preguntas sobre fabricante
        "manufacturer Atarax 25mg Tablet",
        "fabricante Azee 500 Tablet",
        "who makes Anovate Cream",
        # Preguntas más naturales
        "tell me about Allegra-M Tablet",
        "información sobre Ascoril D Plus Syrup",
        "what can you tell me about Alex Syrup",
        # Preguntas específicas
        "is Armotraz Tablet safe",
        "how to use Augmentin Duo Oral Suspension",
        "dosage of Albendazole 400mg Tablet",
        # Preguntas combinadas
        "composition and uses of Arkamin Tablet",
        "side effects and manufacturer of Allegra 180mg Tablet",
    ]
    print("\n" + "="*80)
    print("TESTING DEL MODELO DE MEDICAMENTOS")
    print("="*80)
    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i:2d}] Pregunta: {question}")
        response, method = generate_response(question, tokenizer, model, medicine_data, device)
        print(f"     Respuesta ({method}): {response}")
        print("-" * 60)
    # Modo interactivo
    print("\n" + "="*80)
    print("MODO INTERACTIVO")
    print("="*80)
    print("Algunos medicamentos disponibles:")
    sample_medicines = [
        "Avastin 400mg Injection", "Augmentin 625 Duo Tablet", "Azithral 500 Tablet",
        "Ascoril LS Syrup", "Aciloc 150 Tablet", "Allegra 120mg Tablet"
    ]
    for med in sample_medicines:
        print(f"  - {med}")
    print("\nEjemplos de preguntas:")
    print("  - 'composition [nombre del medicamento]'")
    print("  - 'uses [nombre del medicamento]'")
    print("  - 'side effects [nombre del medicamento]'")
    print("  - 'manufacturer [nombre del medicamento]'")
    print("\nEscribe 'quit' para salir.")
    while True:
        try:
            question = input("\n🔍 Tu pregunta: ").strip()
            if question.lower() in ['quit', 'salir', 'exit']:
                print("¡Hasta luego!")
                break
            if not question:
                continue
            response, method = generate_response(question, tokenizer, model, medicine_data, device)
            print(f"💊 Respuesta: {response}")
            if method == "direct":
                print("   (Respuesta directa de la base de datos)")
            elif method == "generated":
                print("   (Respuesta generada por el modelo)")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")
 
def quick_test_specific_medicines():
    """Test rápido con medicamentos específicos de tu lista"""
    tokenizer, model, medicine_data, device = load_trained_model()
    # Medicamentos específicos de tu lista
    target_medicines = [
        "Avastin 400mg Injection",
        "Augmentin 625 Duo Tablet", 
        "Azithral 500 Tablet",
        "Ascoril LS Syrup",
        "Aciloc 150 Tablet"
    ]
    question_types = ["composition", "uses", "side effects", "manufacturer"]
    print("\n" + "="*80)
    print("TEST RÁPIDO CON MEDICAMENTOS ESPECÍFICOS")
    print("="*80)
    for medicine in target_medicines:
        print(f"\n🔸 MEDICAMENTO: {medicine}")
        print("-" * 40)
        for q_type in question_types:
            question = f"{q_type} {medicine}"
            response, method = generate_response(question, tokenizer, model, medicine_data, device)
            print(f"  {q_type.upper():12}: {response[:100]}{'...' if len(response) > 100 else ''}")
 
if __name__ == "__main__":
    # Ejecutar test completo
    test_medicine_model()
    # Opcional: ejecutar test rápido
    # quick_test_specific_medicines()