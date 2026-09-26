import os
import requests
from typing import List, Dict, Any, Union
from datetime import datetime
from pymongo.database import Database
from repositories.medicineRepository import MedicineRepository
from models.medicineModel import (
    MedicineInfoAPIResponse,
    MedicineSideEffectsAPIResponse,
    MedicineUsesAPIResponse,
    MedicineInfoResponse,
    MedicineSideEffectsResponse,
    MedicineUsesResponse
)


class MedicineService:
    def __init__(self, db: Database):
        self.repository = MedicineRepository(db)
        self.base_url = os.getenv("DIAGNOSTIC_API_BASE_URL", "http://localhost:2342/api/v1")
    
    async def _call_medicine_api(self, endpoint: str) -> Dict[str, Any]:
        """Make API call to external medicine service"""
        try:
            url = f"{self.base_url}/{endpoint}"
            print(f"Calling API endpoint: {url}")
            
            response = requests.get(url, timeout=30)
            print(f"API Response status code: {response.status_code}")
            
            response.raise_for_status()
            
            try:
                data = response.json()
            except ValueError as e:
                print(f"Invalid JSON response: {response.text}")
                raise Exception(f"Invalid JSON response from API: {str(e)}")
            
            # Validate that we got a dictionary response
            if not isinstance(data, dict):
                print(f"Invalid response type: {type(data)}")
                print(f"Response content: {data}")
                raise Exception(f"Invalid API response format. Expected dictionary, got {type(data)}")
            
            # Log the response for debugging
            print(f"API Response for {endpoint}:", data)
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            raise Exception(f"Error calling medicine API: {str(e)}")
        except ValueError as e:
            print(f"JSON parsing error: {str(e)}")
            raise Exception(f"Invalid JSON response from API: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def create_medicine_info(self, medicine_name: str, current_user: Dict[str, Any] = None) -> MedicineInfoResponse:
        """Get and store medicine information"""
        try:
            print(f"Creating medicine info for: {medicine_name}")
            print(f"Current user: {current_user}")
            
            # Call external API
            api_response = await self._call_medicine_api(f"medicine/{medicine_name}/info")
            print(f"API Response received: {api_response}")
            
            # Validate required fields in API response
            required_fields = ["medicine_name", "description", "uses", "manufacturer", "availability", "warnings"]
            missing_fields = [field for field in required_fields if field not in api_response]
            if missing_fields:
                raise Exception(f"Missing required fields in API response: {', '.join(missing_fields)}")
            
            # Parse API response
            try:
                medicine_info = MedicineInfoAPIResponse(**api_response)
            except Exception as e:
                print(f"Error parsing API response: {str(e)}")
                print(f"API Response that caused error: {api_response}")
                raise Exception(f"Failed to parse API response: {str(e)}")
            
            # Prepare data for database with default values if no user
            medicine_data = {
                "user_id": current_user.get("id") if current_user else "anonymous",
                "username": current_user.get("username") if current_user else "anonymous",
                "medicine_name": medicine_info.medicine_name,
                "description": medicine_info.description,
                "uses": medicine_info.uses,
                "manufacturer": medicine_info.manufacturer,
                "availability": medicine_info.availability,
                "warnings": medicine_info.warnings,
                "mode": "info",
                "created_at": datetime.utcnow()
            }
            
            print(f"Prepared medicine data: {medicine_data}")
            
            # Save to database
            medicine_id = await self.repository.create_medicine_info(medicine_data)
            if not medicine_id:
                raise Exception("Failed to save medicine info to database")
            
            print(f"Medicine saved with ID: {medicine_id}")
            
            # Return response
            response = MedicineInfoResponse(
                id=medicine_id,
                user_id=medicine_data["user_id"],
                username=medicine_data["username"],
                medicine_name=medicine_info.medicine_name,
                description=medicine_info.description,
                uses=medicine_info.uses,
                manufacturer=medicine_info.manufacturer,
                availability=medicine_info.availability,
                warnings=medicine_info.warnings,
                created_at=medicine_data["created_at"]
            )
            
            print(f"Prepared response: {response}")
            return response
            
        except Exception as e:
            print(f"Error in create_medicine_info: {str(e)}")
            raise Exception(f"Failed to get medicine info: {str(e)}")
    
    async def create_medicine_side_effects(self, medicine_name: str, current_user: Dict[str, Any] = None) -> MedicineSideEffectsResponse:
        """Get and store medicine side effects"""
        try:
            # Call external API
            api_response = await self._call_medicine_api(f"medicine/{medicine_name}/side-effects")
            
            # Parse API response
            side_effects = MedicineSideEffectsAPIResponse(**api_response)
            
            # Prepare data for database
            medicine_data = {
                "user_id": current_user.get("id") if current_user else "anonymous",
                "username": current_user.get("username") if current_user else "anonymous",
                "medicine_name": side_effects.medicine_name,
                "common_side_effects": side_effects.common_side_effects,
                "serious_side_effects": side_effects.serious_side_effects,
                "rare_side_effects": side_effects.rare_side_effects,
                "warnings": side_effects.warnings,
                "mode": "side_effects",
                "created_at": datetime.utcnow()
            }
            
            # Save to database
            medicine_id = await self.repository.create_medicine_side_effects(medicine_data)
            if not medicine_id:
                raise Exception("Failed to save medicine side effects to database")
            
            # Return response
            return MedicineSideEffectsResponse(
                id=medicine_id,
                user_id=medicine_data["user_id"],
                username=medicine_data["username"],
                medicine_name=side_effects.medicine_name,
                common_side_effects=side_effects.common_side_effects,
                serious_side_effects=side_effects.serious_side_effects,
                rare_side_effects=side_effects.rare_side_effects,
                warnings=side_effects.warnings,
                created_at=medicine_data["created_at"]
            )
            
        except Exception as e:
            raise Exception(f"Failed to get medicine side effects: {str(e)}")
    
    async def create_medicine_uses(self, medicine_name: str, current_user: Dict[str, Any] = None) -> MedicineUsesResponse:
        """Get and store medicine uses"""
        try:
            # Call external API
            api_response = await self._call_medicine_api(f"medicine/{medicine_name}/uses")
            
            # Parse API response
            medicine_uses = MedicineUsesAPIResponse(**api_response)
            
            # Prepare data for database
            medicine_data = {
                "user_id": current_user.get("id") if current_user else "anonymous",
                "username": current_user.get("username") if current_user else "anonymous",
                "medicine_name": medicine_uses.medicine_name,
                "primary_uses": medicine_uses.primary_uses,
                "secondary_uses": medicine_uses.secondary_uses,
                "conditions_treated": medicine_uses.conditions_treated,
                "dosage_info": medicine_uses.dosage_info,
                "mode": "uses",
                "created_at": datetime.utcnow()
            }
            
            # Save to database
            medicine_id = await self.repository.create_medicine_uses(medicine_data)
            if not medicine_id:
                raise Exception("Failed to save medicine uses to database")
            
            # Return response
            return MedicineUsesResponse(
                id=medicine_id,
                user_id=medicine_data["user_id"],
                username=medicine_data["username"],
                medicine_name=medicine_uses.medicine_name,
                primary_uses=medicine_uses.primary_uses,
                secondary_uses=medicine_uses.secondary_uses,
                conditions_treated=medicine_uses.conditions_treated,
                dosage_info=medicine_uses.dosage_info,
                created_at=medicine_data["created_at"]
            )
            
        except Exception as e:
            raise Exception(f"Failed to get medicine uses: {str(e)}")
    
    async def get_user_medicines(self, current_user: Dict[str, Any], limit: int = 20, skip: int = 0, mode: str = None) -> List[Union[MedicineInfoResponse, MedicineSideEffectsResponse, MedicineUsesResponse]]:
        """Get user's medicine records with pagination and optional mode filter"""
        try:
            medicines = await self.repository.get_medicines_by_user_id(
                current_user["id"], limit, skip, mode
            )
            
            result = []
            for medicine in medicines:
                if medicine.get("mode") == "info":
                    result.append(MedicineInfoResponse(**medicine))
                elif medicine.get("mode") == "side_effects":
                    result.append(MedicineSideEffectsResponse(**medicine))
                elif medicine.get("mode") == "uses":
                    result.append(MedicineUsesResponse(**medicine))
            
            return result
        except Exception as e:
            raise Exception(f"Failed to get user medicines: {str(e)}")
    
    async def get_medicine_by_id(self, medicine_id: str, current_user: Dict[str, Any]) -> Union[MedicineInfoResponse, MedicineSideEffectsResponse, MedicineUsesResponse, None]:
        """Get a specific medicine by ID (only if it belongs to current user)"""
        try:
            medicine = await self.repository.get_medicine_by_id(medicine_id)
            
            if not medicine or medicine.get("user_id") != current_user["id"]:
                return None
            
            if medicine.get("mode") == "info":
                return MedicineInfoResponse(**medicine)
            elif medicine.get("mode") == "side_effects":
                return MedicineSideEffectsResponse(**medicine)
            elif medicine.get("mode") == "uses":
                return MedicineUsesResponse(**medicine)
            
            return None
        except Exception as e:
            raise Exception(f"Failed to get medicine by ID: {str(e)}")
    
    async def count_user_medicines(self, current_user: Dict[str, Any], mode: str = None) -> int:
        """Count user's medicines with optional mode filter"""
        try:
            return await self.repository.count_medicines_by_user_id(current_user["id"], mode)
        except Exception as e:
            raise Exception(f"Failed to count user medicines: {str(e)}")
    
    async def delete_medicine(self, medicine_id: str, current_user: Dict[str, Any]) -> bool:
        """Delete a medicine (only if it belongs to current user)"""
        try:
            return await self.repository.delete_medicine(medicine_id, current_user["id"])
        except Exception as e:
            raise Exception(f"Failed to delete medicine: {str(e)}")
    
    async def search_medicines_by_name(self, medicine_name: str, current_user: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search user's medicines by name"""
        try:
            return await self.repository.get_medicines_by_medicine_name(
                medicine_name, current_user["id"]
            )
        except Exception as e:
            raise Exception(f"Failed to search medicines: {str(e)}")
    
    async def get_medicine_stats(self) -> Dict[str, Any]:
        """Get medicine statistics (admin function)"""
        try:
            return await self.repository.get_all_medicines_stats()
        except Exception as e:
            raise Exception(f"Failed to get medicine stats: {str(e)}")