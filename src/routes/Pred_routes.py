from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import os
import requests
from io import BytesIO
from controller.Pred_controller import generate_prediction_plot
from controller.detail_controller import generate_disease_details

router = APIRouter()

from pydantic import BaseModel

class ImageUrlRequest(BaseModel):
    image_url: str

@router.post("/predict-image")
async def predict_image_url(request: ImageUrlRequest):
    try:
        # Fetch the image from the URL
        response = requests.get(request.image_url)
        response.raise_for_status()
        
        # Rest of your code remains the same
        image_content = response.content
        image_id, top_5_list = generate_prediction_plot(image_content)
        
        return JSONResponse(content={
            "image_url": f"/predict-image/{image_id}",
            "top_5_diseases": top_5_list
        })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image from URL: {str(e)}")

# @router.get("/predict-image/{image_id}")
# async def get_prediction_image(image_id: str):
#     image_path = os.path.join("tmp_predictions", f"{image_id}.png")
#     if not os.path.isfile(image_path):
#         raise HTTPException(status_code=404, detail="Image not found")
#     return StreamingResponse(open(image_path, "rb"), media_type="image/png")

@router.get("/disease-details/{disease_name}")
async def get_disease_details(disease_name: str, language: str = "en"):
    details = generate_disease_details(disease_name, language)
    return JSONResponse(content=details)