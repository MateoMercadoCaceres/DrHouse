from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Dict, Any, Union, Optional
from pymongo.database import Database
from config.database import get_database
from services.medicineServices import MedicineService
from models.medicineModel import (
    MedicineRequest, 
    MedicineInfoRequest, 
    MedicineSideEffectsRequest,
    MedicineUsesRequest,
    MedicineInfoResponse, 
    MedicineSideEffectsResponse, 
    MedicineUsesResponse,
    MedicineMode
)
from middleware.jwtMiddleware import get_current_user

router = APIRouter(
    prefix="/api/medicines",
    tags=["medicines"]
)

def get_medicine_service(db: Database = Depends(get_database)) -> MedicineService:
    """Dependency to get MedicineService instance"""
    return MedicineService(db)

async def get_optional_user(current_user: Optional[Dict[str, Any]] = Depends(get_current_user)) -> Optional[Dict[str, Any]]:
    """Dependency to get current user if available"""
    return current_user

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_medicine_query(
    request: MedicineRequest,
    current_user: Optional[Dict[str, Any]] = Depends(get_optional_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
) -> Union[MedicineInfoResponse, MedicineSideEffectsResponse, MedicineUsesResponse]:
    """
    Create a new medicine query based on mode (info, side_effects, uses)
    """
    try:
        if request.mode == MedicineMode.INFO:
            return await medicine_service.create_medicine_info(request.medicine_name, current_user)
        elif request.mode == MedicineMode.SIDE_EFFECTS:
            return await medicine_service.create_medicine_side_effects(request.medicine_name, current_user)
        elif request.mode == MedicineMode.USES:
            return await medicine_service.create_medicine_uses(request.medicine_name, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid medicine query mode"
            )
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in create_medicine_query endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create medicine query: {error_message}"
        )

@router.post("/info", response_model=MedicineInfoResponse, status_code=status.HTTP_201_CREATED)
async def get_medicine_info(
    request: MedicineInfoRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Get medicine information
    """
    try:
        info_result = await medicine_service.create_medicine_info(request.medicine_name, current_user)
        return info_result
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in get_medicine_info endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get medicine info: {error_message}"
        )

@router.post("/side-effects", response_model=MedicineSideEffectsResponse, status_code=status.HTTP_201_CREATED)
async def get_medicine_side_effects(
    request: MedicineSideEffectsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Get medicine side effects
    """
    try:
        side_effects_result = await medicine_service.create_medicine_side_effects(request.medicine_name, current_user)
        return side_effects_result
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in get_medicine_side_effects endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get medicine side effects: {error_message}"
        )

@router.post("/uses", response_model=MedicineUsesResponse, status_code=status.HTTP_201_CREATED)
async def get_medicine_uses(
    request: MedicineUsesRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Get medicine uses and dosage information
    """
    try:
        uses_result = await medicine_service.create_medicine_uses(request.medicine_name, current_user)
        return uses_result
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in get_medicine_uses endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get medicine uses: {error_message}"
        )

@router.get("/", response_model=List[Union[MedicineInfoResponse, MedicineSideEffectsResponse, MedicineUsesResponse]])
async def get_user_medicines(
    limit: int = Query(20, ge=1, le=100, description="Number of medicine queries to return"),
    skip: int = Query(0, ge=0, description="Number of medicine queries to skip"),
    mode: str = Query(None, description="Filter by medicine query mode (info, side_effects, uses)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Get all medicine queries for the current user with pagination and optional mode filter
    """
    try:
        medicines = await medicine_service.get_user_medicines(current_user, limit, skip, mode)
        return medicines
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/count")
async def get_user_medicines_count(
    mode: str = Query(None, description="Filter by medicine query mode (info, side_effects, uses)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Get total count of medicine queries for the current user with optional mode filter
    """
    try:
        count = await medicine_service.count_user_medicines(current_user, mode)
        return {"count": count}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/search/{medicine_name}")
async def search_medicines_by_name(
    medicine_name: str = Path(..., description="Medicine name to search for"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Search user's previous medicine queries by medicine name
    """
    try:
        medicines = await medicine_service.search_medicines_by_name(medicine_name, current_user)
        return {"medicines": medicines}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{medicine_id}")
async def get_medicine(
    medicine_id: str = Path(..., description="ID of the medicine query to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    medicine_service: MedicineService = Depends(get_medicine_service)
):
    """
    Get a specific medicine query by ID
    """
    try:
        medicine = await medicine_service.get_medicine_by_id(medicine_id, current_user)
        return medicine
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )