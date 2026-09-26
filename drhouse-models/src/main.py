from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv 
import os
from controllers.diagnosticController import router as diagnostic_router
from controllers.medicineController import router as medicine_router
from controllers.imageController import router as image_router

load_dotenv()

app = FastAPI(
    title="API de Diagnóstico Médico",
    description="API para diagnóstico médico usando DeepSeek AI y generación de imágenes de medicamentos con Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rutas
app.include_router(diagnostic_router, prefix="/api/v1", tags=["Diagnóstico"])
app.include_router(medicine_router, prefix="/api/v1", tags=["Medicina"])
app.include_router(image_router, prefix="/api/v1", tags=["Imágenes de Medicamentos"])

@app.get("/")
async def root():
    return {
        "message": "API de Diagnóstico Médico con DeepSeek y Generación de Imágenes con Gemini",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "medicine_info": "/api/v1/medicine/{medicine_name}/info",
            "side_effects": "/api/v1/medicine/{medicine_name}/side-effects",
            "medicine_uses": "/api/v1/medicine/{medicine_name}/uses",
            "recommend_medicine": "/api/v1/medicine/recommend",
            "generate_medicine_image": "/api/v1/medicine/generate-image",
            "get_medicine_image_info": "/api/v1/medicine/images/{filename}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)