from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from controller.controller import generate_prediction_plot

router = APIRouter()

@router.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    image_buffer = generate_prediction_plot(contents)
    return StreamingResponse(image_buffer, media_type="image/png")