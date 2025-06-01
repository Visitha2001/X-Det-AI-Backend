# routes/image_upload.py
from fastapi import APIRouter, UploadFile, File, Depends, status
from fastapi.responses import JSONResponse
from controller.cloudinary_service import CloudinaryService
from models.image_upload import CloudinaryUploadResult

router = APIRouter(
    prefix="/images",
    tags=["images"]
)

@router.post("/upload", response_model=CloudinaryUploadResult, status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image to Cloudinary
    
    - **file**: Image file to upload (JPEG, PNG, etc.)
    """
    # Check if the file is an image
    if not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Only image files are allowed"}
        )
    
    # Upload to Cloudinary
    upload_result = await CloudinaryService.upload_image(file)
    
    # Here you would typically save the result to your database
    # For example:
    # db_image = crud.create_image(db, image=ImageUploadCreate(**upload_result))
    
    return upload_result

@router.delete("/{public_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(public_id: str):
    """
    Delete an image from Cloudinary
    
    - **public_id**: The public_id of the image to delete
    """
    await CloudinaryService.delete_image(public_id)
    return None