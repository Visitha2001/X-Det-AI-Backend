from pydantic import BaseModel

class CloudinaryUploadResult(BaseModel):
    public_id: str
    url: str
    secure_url: str
    format: str
    width: int
    height: int

class ImageUploadInDB(CloudinaryUploadResult):
    id: int
    
    class Config:
        orm_mode = True