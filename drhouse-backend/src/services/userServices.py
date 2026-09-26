from typing import Optional, Dict, Any
from datetime import datetime
from pymongo.database import Database
from repositories.userRepository import UserRepository
from services.authServices import AuthService
from models.userModel import UserCreate, UserResponse, Token

class UserService:
    def __init__(self, db: Database):
        self.user_repository = UserRepository(db)
        self.auth_service = AuthService()

    async def register_user(self, user_create: UserCreate) -> Optional[UserResponse]:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_username(user_create.username)
        if existing_user:
            raise ValueError("Username already exists")
        
        existing_email = await self.user_repository.get_user_by_email(user_create.email)
        if existing_email:
            raise ValueError("Email already exists")

        # Hash password and create user
        hashed_password = self.auth_service.hash_password(user_create.password)
        
        user_data = {
            "username": user_create.username,
            "email": user_create.email,
            "full_name": user_create.full_name,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "is_active": True
        }

        user_id = await self.user_repository.create_user(user_data)
        if not user_id:
            return None

        # Return user without password
        user_data["_id"] = user_id
        del user_data["hashed_password"]
        return UserResponse(**user_data)

    async def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data"""
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            return None
        
        if not self.auth_service.verify_password(password, user["hashed_password"]):
            return None
        
        if not user["is_active"]:
            return None
        
        return user

    async def login_user(self, username: str, password: str) -> Optional[Token]:
        """Login user and return JWT token"""
        user = await self.authenticate_user(username, password)
        if not user:
            return None

        access_token = self.auth_service.create_access_token(
            data={"sub": user["username"]}
        )
        
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Get current user from JWT token"""
        username = self.auth_service.verify_token(token)
        if not username:
            return None
        
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            return None
        
        del user["hashed_password"]
        return UserResponse(**user)
