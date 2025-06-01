from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, validator, Field

class DiseaseProbability(BaseModel):
    disease: str = Field(..., description="Name of the disease")
    probability: float = Field(..., ge=0, le=1, description="Probability score between 0 and 1")

class PredictionData(BaseModel):
    image_url: str = Field(..., description="URL of the analyzed image")
    top_5_diseases: List[DiseaseProbability] = Field(..., min_items=1, max_items=5)

class DiseaseInfo(BaseModel):
    disease: str = Field(..., description="Name of the disease")
    details: str = Field(..., description="Detailed information about the disease")

class ResultCreate(BaseModel):
    username: str = Field(..., description="Username who requested the prediction")
    disease_details: DiseaseInfo
    prediction_data: PredictionData
    image_url: str = Field(..., description="URL of the original image")
    details: str = Field(..., description="Additional details about the result")
    disease: str = Field(..., description="Primary diagnosed disease")
    timestamp: Union[datetime, str] = Field(default_factory=lambda: datetime.utcnow())

    @validator('timestamp', pre=True)
    def parse_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid timestamp format: {str(e)}")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "username": "user123",
                "disease_details": {
                    "disease": "Tomato Early Blight",
                    "details": "Early blight is caused by the fungus..."
                },
                "prediction_data": {
                    "image_url": "https://example.com/image.jpg",
                    "top_5_diseases": [
                        {"disease": "Tomato Early Blight", "probability": 0.95},
                        {"disease": "Tomato Late Blight", "probability": 0.03}
                    ]
                },
                "image_url": "https://example.com/original.jpg",
                "details": "Found in leaf examination",
                "disease": "Tomato Early Blight",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }