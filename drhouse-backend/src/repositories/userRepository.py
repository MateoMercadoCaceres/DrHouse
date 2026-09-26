from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import Optional, Dict, Any
from models.userModel import User, UserCreate

class UserRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db.users

    async def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user and return the user ID"""
        try:
            result = self.collection.insert_one(user_data)
            return str(result.inserted_id)
        except DuplicateKeyError:
            return None

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        user = self.collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        user = self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except:
            return None

    async def update_user_activity(self, user_id: str, is_active: bool) -> bool:
        """Update user active status"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": is_active}}
            )
            return result.modified_count > 0
        except:
            return False
