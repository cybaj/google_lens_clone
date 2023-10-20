from pydantic import BaseModel

class TranslationRequest(BaseModel):
    target_language: str
    file: bytes

class TranslationResponse(BaseModel):
    result_image: str  # Assuming you'll return the image as a base64 encoded string or a URL

