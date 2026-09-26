from pydantic import BaseModel

class ImageGenerationRequest(BaseModel):
    medicine_name: str
    description: str | None = None

class ImageGenerationResponse(BaseModel):
    filename: str
    image_url: str
    dimensions: tuple[int, int]
    format: str
    color_mode: str
