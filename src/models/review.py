from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Review(BaseModel):
    username: str
    content: str
    rating: int
    created_at: Optional[datetime] = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "content": "Great product!",
                "rating": 5
            }
        }