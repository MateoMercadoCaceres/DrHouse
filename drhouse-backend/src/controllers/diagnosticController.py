from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Union
from pymongo.database import Database
from config.database import get_database
from services.diagnosticServices import DiagnosticService
from models.diagnosticModel import (
    DiagnosticRequest, 
    SymptomsRequest, 
    ExplainDiseaseRequest,
    DiagnosticResponse, 
    SymptomsResponse, 
    ExplainDiseaseResponse,
    DiagnosticMode
)
from middleware.jwtMiddleware import get_current_user

router = APIRouter(
    prefix="/api/diagnostics",
    tags=["diagnostics"]
)

def get_diagnostic_service(db: Database = Depends(get_database)) -> DiagnosticService:
    """Dependency to get DiagnosticService instance"""
    return DiagnosticService(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_diagnostic(
    request: DiagnosticRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
) -> Union[DiagnosticResponse, SymptomsResponse, ExplainDiseaseResponse]:
    """
    Create a new diagnostic, symptoms extraction, or disease explanation based on mode
    """
    try:
        if request.mode == DiagnosticMode.DIAGNOSE:
            return await diagnostic_service.create_diagnostic(request.user_input, current_user)
        elif request.mode == DiagnosticMode.SYMPTOMS:
            return await diagnostic_service.create_symptoms_extraction(request.user_input, current_user)
        elif request.mode == DiagnosticMode.EXPLAIN:
            return await diagnostic_service.create_disease_explanation(request.user_input, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid diagnostic mode"
            )
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in create_diagnostic endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create diagnostic: {error_message}"
        )

@router.post("/symptoms", response_model=SymptomsResponse, status_code=status.HTTP_201_CREATED)
async def extract_symptoms(
    request: SymptomsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
):
    """
    Extract symptoms from user input
    """
    try:
        symptoms_result = await diagnostic_service.create_symptoms_extraction(request.user_input, current_user)
        return symptoms_result
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in extract_symptoms endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract symptoms: {error_message}"
        )

@router.post("/explain-disease", response_model=ExplainDiseaseResponse, status_code=status.HTTP_201_CREATED)
async def explain_disease(
    request: ExplainDiseaseRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
):
    """
    Explain a specific disease or diagnosis
    """
    try:
        explanation_result = await diagnostic_service.create_disease_explanation(request.diagnosis, current_user)
        return explanation_result
        
    except Exception as e:
        error_message = str(e)
        print(f"Error in explain_disease endpoint: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain disease: {error_message}"
        )

@router.get("/", response_model=List[Union[DiagnosticResponse, SymptomsResponse, ExplainDiseaseResponse]])
async def get_user_diagnostics(
    limit: int = Query(20, ge=1, le=100, description="Number of diagnostics to return"),
    skip: int = Query(0, ge=0, description="Number of diagnostics to skip"),
    mode: str = Query(None, description="Filter by diagnostic mode (diagnose, symptoms, explain)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
):
    """
    Get all diagnostics for the current user with pagination and optional mode filter
    """
    try:
        diagnostics = await diagnostic_service.get_user_diagnostics(current_user, limit, skip, mode)
        return diagnostics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/count")
async def get_user_diagnostics_count(
    mode: str = Query(None, description="Filter by diagnostic mode (diagnose, symptoms, explain)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
):
    """
    Get total count of diagnostics for the current user with optional mode filter
    """
    try:
        count = await diagnostic_service.count_user_diagnostics(current_user, mode)
        return {"count": count}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{diagnostic_id}")
async def get_diagnostic(
    diagnostic_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
) -> Union[DiagnosticResponse, SymptomsResponse, ExplainDiseaseResponse]:
    """
    Get a specific diagnostic by ID (only if it belongs to current user)
    """
    try:
        diagnostic = await diagnostic_service.get_diagnostic_by_id(diagnostic_id, current_user)
        if not diagnostic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnostic not found or you don't have permission to access it"
            )
        
        return diagnostic
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/{diagnostic_id}")
async def delete_diagnostic(
    diagnostic_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    diagnostic_service: DiagnosticService = Depends(get_diagnostic_service)
):
    """
    Delete a specific diagnostic by ID (only if it belongs to current user)
    """
    try:
        success = await diagnostic_service.delete_diagnostic(diagnostic_id, current_user)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnostic not found or you don't have permission to delete it"
            )
        
        return {"message": "Diagnostic deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )