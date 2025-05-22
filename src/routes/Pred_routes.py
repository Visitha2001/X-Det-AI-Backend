from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import os
from controller.Pred_controller import generate_prediction_plot
from controller.detail_controller import generate_disease_details

router = APIRouter()

@router.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    image_id, top_5_list = generate_prediction_plot(contents)
    return JSONResponse(content={
        "image_url": f"/predict-image/{image_id}",
        "top_5_diseases": top_5_list
    })

@router.get("/predict-image/{image_id}")
async def get_prediction_image(image_id: str):
    image_path = os.path.join("tmp_predictions", f"{image_id}.png")
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return StreamingResponse(open(image_path, "rb"), media_type="image/png")

@router.get("/disease-details/{disease_name}")
async def get_disease_details(disease_name: str):
    details = generate_disease_details(disease_name)
    return JSONResponse(content=details)