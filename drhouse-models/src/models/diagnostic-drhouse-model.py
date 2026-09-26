from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
 
# Ruta del modelo entrenado
model_path = "./gpt2-medical"
 
# Cargar tokenizer y modelo
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
 
# Agregar token de padding
tokenizer.pad_token = tokenizer.eos_token
 
# Modo evaluación
model.eval()
 
# Texto de entrada (puedes modificarlo)
symptoms_text = "itching, skin rash, nodal skin eruptions"
 
# Crear prompt bien delimitado
prompt = f"Síntomas: {symptoms_text} | Diagnóstico:"
 
# Tokenizar prompt
inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=True)
 
# Generar texto a partir del prompt
with torch.no_grad():
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=inputs["input_ids"].shape[1] + 30,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
 
# Decodificar salida
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
 
# Extraer diagnóstico delimitado después de "| Diagnóstico:"
if "| Diagnóstico:" in generated_text:
    diagnosis_part = generated_text.split("| Diagnóstico:")[-1]
    diagnosis = diagnosis_part.split("|")[0].strip().split(".")[0]
else:
    diagnosis = "No se pudo generar diagnóstico."
 
 
# Mostrar resultado
print("=== Diagnóstico generado por GPT-2 ===")
print(f"🧠 {diagnosis}")