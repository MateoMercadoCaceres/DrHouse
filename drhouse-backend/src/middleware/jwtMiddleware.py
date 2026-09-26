from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from services.authServices import AuthService
from services.userServices import UserService
from config.database import get_database
from pymongo.database import Database
from typing import Optional, Dict, Any

security = HTTPBearer()

def get_user_service(db: Database = Depends(get_database)) -> UserService:
    """Dependency to get UserService instance"""
    return UserService(db)

def get_auth_service() -> AuthService:
    """Dependency to get AuthService instance"""
    return AuthService()

async def get_current_user(
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
    
    user = await user_service.user_repository.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.auth_service = AuthService()
        # Rutas que no requieren autenticación
        self.exclude_paths = exclude_paths or [
            "/api/users/register",
            "/api/users/login",
            "/api/medicines",  # Endpoint para crear consultas de medicamentos
            "/docs",
            "/redoc",
            "/openapi.json",
            "/"
        ]

    async def dispatch(self, request: Request, call_next):
        # Verificar si la ruta está excluida de la autenticación
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            response = await call_next(request)
            return response

        # Obtener el token del header Authorization
        authorization = request.headers.get("Authorization")
        
        if not authorization or not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Authorization header missing or invalid format",
                    "headers": {"WWW-Authenticate": "Bearer"}
                }
            )

        # Extraer el token
        token = authorization.split(" ")[1]
        
        # Verificar el token
        username = self.auth_service.verify_token(token)
        if not username:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid or expired token",
                    "headers": {"WWW-Authenticate": "Bearer"}
                }
            )

        # Agregar el username al estado de la request para uso posterior
        request.state.current_user = username
        
        response = await call_next(request)
        return response