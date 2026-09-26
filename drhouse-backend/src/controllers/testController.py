from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.userServices import UserService
from services.authServices import AuthService
from config.database import get_database
from pymongo.database import Database
from typing import Dict, Any

router = APIRouter(prefix="/api/test", tags=["Test"])
security = HTTPBearer()

def get_user_service(db: Database = Depends(get_database)) -> UserService:
    """Dependency to get UserService instance"""
    return UserService(db)

def get_auth_service() -> AuthService:
    """Dependency to get AuthService instance"""
    return AuthService()

async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service)
) -> Dict[str, Any]:
    """Dependency to get current user from JWT token"""
    username = auth_service.verify_token(credentials.credentials)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener datos completos del usuario
    user = await user_service.user_repository.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.get("/protected")
async def protected_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user_from_token)
):
    """
    Endpoint protegido que requiere autenticación JWT.
    Para probar en Postman:
    1. Hacer login en /api/users/login para obtener el token
    2. En Headers agregar: Authorization: Bearer {tu_token_aqui}
    3. Hacer GET a este endpoint
    """
    return {
        "message": "¡Acceso autorizado!",
        "user_info": {
            "username": current_user.get("username"),
            "email": current_user.get("email"),
            "full_name": current_user.get("full_name"),
            "is_active": current_user.get("is_active"),
            "created_at": current_user.get("created_at")
        },
        "endpoint": "/api/test/protected"
    }

@router.get("/public")
async def public_endpoint():
    """
    Endpoint público que NO requiere autenticación.
    Puede ser accedido sin token.
    """
    return {
        "message": "Este es un endpoint público",
        "requires_auth": False,
        "endpoint": "/api/test/public"
    }

@router.get("/user-info")
async def get_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user_from_token)
):
    """
    Endpoint que devuelve información detallada del usuario autenticado.
    Requiere Bearer token en el header Authorization.
    """
    return {
        "message": "Información del usuario autenticado",
        "user": {
            "id": str(current_user.get("_id")),
            "username": current_user.get("username"),
            "email": current_user.get("email"),
            "full_name": current_user.get("full_name"),
            "is_active": current_user.get("is_active"),
            "created_at": current_user.get("created_at").isoformat() if current_user.get("created_at") else None
        }
    }

@router.get("/middleware-test")
async def middleware_test(request: Request):
    """
    Endpoint para probar el middleware JWT.
    Si el middleware está activo, solo funcionará con token válido.
    """
    # Si el middleware está activo, current_user estará disponible en request.state
    current_user = getattr(request.state, 'current_user', None)
    
    return {
        "message": "Endpoint protegido por middleware",
        "middleware_user": current_user,
        "headers_received": dict(request.headers),
        "endpoint": "/api/test/middleware-test"
    }