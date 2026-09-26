from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime

class MedicineRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.medicines

    async def create_medicine_info(self, medicine_data: Dict[str, Any]) -> Optional[str]:
        """Create a new medicine info record"""
        try:
            result = self.collection.insert_one(medicine_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating medicine info: {e}")
            return None

    async def create_medicine_side_effects(self, side_effects_data: Dict[str, Any]) -> Optional[str]:
        """Create a new medicine side effects record"""
        try:
            result = self.collection.insert_one(side_effects_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating medicine side effects: {e}")
            return None

    async def create_medicine_uses(self, uses_data: Dict[str, Any]) -> Optional[str]:
        """Create a new medicine uses record"""
        try:
            result = self.collection.insert_one(uses_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating medicine uses: {e}")
            return None

    async def get_medicine_by_id(self, medicine_id: str) -> Optional[Dict[str, Any]]:
        """Get medicine by ID"""
        try:
            medicine = self.collection.find_one({"_id": ObjectId(medicine_id)})
            if medicine:
                medicine["_id"] = str(medicine["_id"])
            return medicine
        except Exception as e:
            print(f"Error getting medicine by ID: {e}")
            return None

    async def get_medicines_by_user_id(self, user_id: str, limit: int = 20, skip: int = 0, mode: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get medicines by user ID with pagination and optional mode filter"""
        try:
            # Construir filtro
            filter_query = {"user_id": user_id}
            if mode:
                filter_query["mode"] = mode
            
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            medicines = []
            for medicine in cursor:
                medicine["_id"] = str(medicine["_id"])
                medicines.append(medicine)
            
            return medicines
        except Exception as e:
            print(f"Error getting medicines by user ID: {e}")
            return []

    async def get_medicines_by_username(self, username: str, limit: int = 20, skip: int = 0, mode: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get medicines by username with pagination and optional mode filter"""
        try:
            # Construir filtro
            filter_query = {"username": username}
            if mode:
                filter_query["mode"] = mode
            
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            medicines = []
            for medicine in cursor:
                medicine["_id"] = str(medicine["_id"])
                medicines.append(medicine)
            
            return medicines
        except Exception as e:
            print(f"Error getting medicines by username: {e}")
            return []

    async def get_medicines_by_medicine_name(self, medicine_name: str, user_id: str, limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        """Get all records for a specific medicine by a user"""
        try:
            filter_query = {
                "medicine_name": {"$regex": medicine_name, "$options": "i"},
                "user_id": user_id
            }
            
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            medicines = []
            for medicine in cursor:
                medicine["_id"] = str(medicine["_id"])
                medicines.append(medicine)
            
            return medicines
        except Exception as e:
            print(f"Error getting medicines by medicine name: {e}")
            return []

    async def count_medicines_by_user_id(self, user_id: str, mode: Optional[str] = None) -> int:
        """Count total medicines for a user with optional mode filter"""
        try:
            filter_query = {"user_id": user_id}
            if mode:
                filter_query["mode"] = mode
            
            return self.collection.count_documents(filter_query)
        except Exception as e:
            print(f"Error counting medicines: {e}")
            return 0

    async def count_medicines_by_username(self, username: str, mode: Optional[str] = None) -> int:
        """Count total medicines for a username with optional mode filter"""
        try:
            filter_query = {"username": username}
            if mode:
                filter_query["mode"] = mode
            
            return self.collection.count_documents(filter_query)
        except Exception as e:
            print(f"Error counting medicines by username: {e}")
            return 0

    async def delete_medicine(self, medicine_id: str, user_id: str) -> bool:
        """Delete medicine (only if belongs to user)"""
        try:
            result = self.collection.delete_one({
                "_id": ObjectId(medicine_id),
                "user_id": user_id
            })
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting medicine: {e}")
            return False

    async def get_medicines_by_mode(self, mode: str, limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        """Get medicines by mode (admin function)"""
        try:
            cursor = self.collection.find({"mode": mode})
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            
            medicines = []
            for medicine in cursor:
                medicine["_id"] = str(medicine["_id"])
                medicines.append(medicine)
            
            return medicines
        except Exception as e:
            print(f"Error getting medicines by mode: {e}")
            return []

    async def get_all_medicines_stats(self) -> Dict[str, Any]:
        """Get statistics about all medicines"""
        try:
            total = self.collection.count_documents({})
            info_count = self.collection.count_documents({"mode": "info"})
            side_effects_count = self.collection.count_documents({"mode": "side_effects"})
            uses_count = self.collection.count_documents({"mode": "uses"})
            
            return {
                "total": total,
                "by_mode": {
                    "info": info_count,
                    "side_effects": side_effects_count,
                    "uses": uses_count
                }
            }
        except Exception as e:
            print(f"Error getting medicines stats: {e}")
            return {
                "total": 0,
                "by_mode": {
                    "info": 0,
                    "side_effects": 0,
                    "uses": 0
                }
            }

    async def search_medicines_by_name(self, medicine_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search medicines by name (for suggestions/autocomplete)"""
        try:
            # Buscar por nombre de medicina usando regex case-insensitive
            cursor = self.collection.find({
                "medicine_name": {"$regex": medicine_name, "$options": "i"}
            }).limit(limit)
            
            medicines = []
            medicine_names = set()  # Para evitar duplicados
            
            for medicine in cursor:
                medicine_name_value = medicine.get("medicine_name", "")
                if medicine_name_value not in medicine_names:
                    medicine["_id"] = str(medicine["_id"])
                    medicines.append(medicine)
                    medicine_names.add(medicine_name_value)
            
            return medicines
        except Exception as e:
            print(f"Error searching medicines by name: {e}")
            return []