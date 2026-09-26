from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import base64
from prompt.imagePrompt import generate_medicine_image_prompt
from models.imageSchema import ImageGenerationResponse

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=api_key)


class ImageService:
    @staticmethod
    async def generate_medicine_image(medicine_name: str, description: str | None = None) -> ImageGenerationResponse:
        prompt = generate_medicine_image_prompt(medicine_name, description)
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
           
            if not response.candidates or len(response.candidates) == 0:
                raise Exception("No candidates received from Gemini API")
            
            candidate = response.candidates[0]
            if not candidate.content or not candidate.content.parts:
                raise Exception("No valid content in response")
            

            for part in candidate.content.parts:
                if part.inline_data is not None and part.inline_data.data:
                    image_data = part.inline_data.data
                    image_bytes = BytesIO(image_data)
                    image_bytes.seek(0)

                    try:
                        image = Image.open(image_bytes)
                        image = image.convert("RGBA")  # Aumentamos compatibilidad
                    except Exception:
                        try:
                            image_bytes.seek(0)
                            raw_data = image_bytes.read()
                            decoded_data = base64.b64decode(raw_data)
                            image = Image.open(BytesIO(decoded_data))
                        except Exception as e:
                            continue

                    # Generar nombre de archivo seguro
                    safe_name = medicine_name.lower().replace(' ', '_').replace("/", "_").replace("\\", "_")
                    filename = f"{safe_name}_package.png"

                    os.makedirs("static/images", exist_ok=True)

                    image_path = f"static/images/{filename}"

                    image.save(image_path, format='PNG')

                    return ImageGenerationResponse(
                        filename=filename,
                        image_url=f"/static/images/{filename}",
                        dimensions=image.size,
                        format=image.format or 'PNG',
                        color_mode=image.mode
                    )

            raise Exception("No se encontró una imagen válida en la respuesta")

        except Exception as e:
            raise Exception(f"Error generando la imagen: {str(e)}")
