from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Review(BaseModel):
    id: Optional[str] = None
    username: str
    content: str
    rating: int
    created_at: Optional[datetime] = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "id": "64d8b9c8e4b9c8e4b9c8e4b9",
                "username": "john_doe",
                "content": "Great product!",
                "rating": 5,
                "created_at": "2023-08-01T00:00:00"
            }
        }