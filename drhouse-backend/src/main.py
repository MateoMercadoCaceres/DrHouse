from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from config.database import connect_to_mongo, close_mongo_connection
from controllers.userController import router as user_router
from controllers.authController import router as auth_router
from controllers.testController import router as test_router
from controllers.diagnosticController import router as diagnostic_router
from controllers.medicineController import router as medicine_router
from middleware.jwtMiddleware import JWTAuthMiddleware

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    connect_to_mongo()
    yield
    # Shutdown
    close_mongo_connection()

app = FastAPI(
    title="DrHouse Diagnostic API",
    description="API REST para diagnóstico médico con IA y autenticación JWT",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(diagnostic_router)
app.include_router(medicine_router)
app.include_router(auth_router)
app.include_router(test_router)

@app.get("/")
async def root():
    return {"message": "DrHouse Diagnostic API is running!", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    port=int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)