from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    # Aquí deberías validar las credenciales contra tu base de datos
    # Por ahora, usaremos credenciales de prueba
    if request.username == "test" and request.password == "test123":
        # Crear el token
        expiration = datetime.utcnow() + timedelta(hours=24)
        token_data = {
            "sub": request.username,
            "exp": expiration.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }
        
        token = jwt.encode(
            token_data,
            os.getenv("JWT_SECRET_KEY"),
            algorithm=os.getenv("JWT_ALGORITHM", "HS256")
        )
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 