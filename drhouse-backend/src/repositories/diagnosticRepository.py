from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime

class DiagnosticRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.diagnostics

    async def create_diagnostic(self, diagnostic_data: Dict[str, Any]) -> Optional[str]:
        """Create a new diagnostic record"""
        try:
            result = self.collection.insert_one(diagnostic_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating diagnostic: {e}")
            return None

    async def create_symptoms(self, symptoms_data: Dict[str, Any]) -> Optional[str]:
        """Create a new symptoms extraction record"""
        try:
            result = self.collection.insert_one(symptoms_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating symptoms: {e}")
            return None

    async def create_disease_explanation(self, explanation_data: Dict[str, Any]) -> Optional[str]:
        """Create a new disease explanation record"""
        try:
            result = self.collection.insert_one(explanation_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating disease explanation: {e}")
            return None

    async def get_diagnostic_by_id(self, diagnostic_id: str) -> Optional[Dict[str, Any]]:
        """Get diagnostic by ID"""
        try:
            diagnostic = self.collection.find_one({"_id": ObjectId(diagnostic_id)})
            if diagnostic:
                diagnostic["_id"] = str(diagnostic["_id"])
            return diagnostic
        except Exception as e:
            print(f"Error getting diagnostic by ID: {e}")
            return None

    async def get_diagnostics_by_user_id(self, user_id: str, limit: int = 20, skip: int = 0, mode: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get diagnostics by user ID with pagination and optional mode filter"""
        try:
            # Construir filtro
            filter_query = {"user_id": user_id}
            if mode:
                filter_query["mode"] = mode
            
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            diagnostics = []
            for diagnostic in cursor:
                diagnostic["_id"] = str(diagnostic["_id"])
                diagnostics.append(diagnostic)
            
            return diagnostics
        except Exception as e:
            print(f"Error getting diagnostics by user ID: {e}")
            return []

    async def get_diagnostics_by_username(self, username: str, limit: int = 20, skip: int = 0, mode: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get diagnostics by username with pagination and optional mode filter"""
        try:
            # Construir filtro
            filter_query = {"username": username}
            if mode:
                filter_query["mode"] = mode
            
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            diagnostics = []
            for diagnostic in cursor:
                diagnostic["_id"] = str(diagnostic["_id"])
                diagnostics.append(diagnostic)
            
            return diagnostics
        except Exception as e:
            print(f"Error getting diagnostics by username: {e}")
            return []

    async def count_diagnostics_by_user_id(self, user_id: str, mode: Optional[str] = None) -> int:
        """Count total diagnostics for a user with optional mode filter"""
        try:
            filter_query = {"user_id": user_id}
            if mode:
                filter_query["mode"] = mode
            
            return self.collection.count_documents(filter_query)
        except Exception as e:
            print(f"Error counting diagnostics: {e}")
            return 0

    async def count_diagnostics_by_username(self, username: str, mode: Optional[str] = None) -> int:
        """Count total diagnostics for a username with optional mode filter"""
        try:
            filter_query = {"username": username}
            if mode:
                filter_query["mode"] = mode
            
            return self.collection.count_documents(filter_query)
        except Exception as e:
            print(f"Error counting diagnostics by username: {e}")
            return 0

    async def delete_diagnostic(self, diagnostic_id: str, user_id: str) -> bool:
        """Delete diagnostic (only if belongs to user)"""
        try:
            result = self.collection.delete_one({
                "_id": ObjectId(diagnostic_id),
                "user_id": user_id
            })
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting diagnostic: {e}")
            return False

    async def get_diagnostics_by_mode(self, mode: str, limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        """Get diagnostics by mode (admin function)"""
        try:
            cursor = self.collection.find({"mode": mode})
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            diagnostics = []
            for diagnostic in cursor:
                diagnostic["_id"] = str(diagnostic["_id"])
                diagnostics.append(diagnostic)
            
            return diagnostics
        except Exception as e:
            print(f"Error getting diagnostics by mode: {e}")
            return []

    async def get_all_diagnostics_stats(self) -> Dict[str, Any]:
        """Get statistics about all diagnostics"""
        try:
            total = self.collection.count_documents({})
            diagnose_count = self.collection.count_documents({"mode": "diagnose"})
            symptoms_count = self.collection.count_documents({"mode": "symptoms"})
            explain_count = self.collection.count_documents({"mode": "explain"})
            
            return {
                "total": total,
                "by_mode": {
                    "diagnose": diagnose_count,
                    "symptoms": symptoms_count,
                    "explain": explain_count
                }
            }
        except Exception as e:
            print(f"Error getting diagnostics stats: {e}")
            return {
                "total": 0,
                "by_mode": {
                    "diagnose": 0,
                    "symptoms": 0,
                    "explain": 0
                }
            }