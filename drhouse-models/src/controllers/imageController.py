from fastapi import APIRouter, HTTPException
from models.imageSchema import ImageGenerationRequest, ImageGenerationResponse
from services.imageService import ImageService

router = APIRouter()

@router.post("/medicine/generate-image", response_model=ImageGenerationResponse)
async def generate_medicine_image(request: ImageGenerationRequest):
    try:
        response = await ImageService.generate_medicine_image(
            medicine_name=request.medicine_name,
            description=request.description
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
