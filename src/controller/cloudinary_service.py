# services/cloudinary_service.py
import cloudinary
import cloudinary.uploader
from models.cloudinary import CloudinarySettings
from fastapi import HTTPException, status

# Configure Cloudinary
config = CloudinarySettings()
cloudinary.config(
    cloud_name=config.cloud_name,
    api_key=config.api_key,
    api_secret=config.api_secret
)

class CloudinaryService:
    @staticmethod
    async def upload_image(file, folder: str = "fastapi_uploads"):
        try:
            # Upload the image
            upload_result = cloudinary.uploader.upload(
                file.file,
                folder=folder
            )
            
            return {
                "public_id": upload_result["public_id"],
                "url": upload_result["url"],
                "secure_url": upload_result["secure_url"],
                "format": upload_result["format"],
                "width": upload_result["width"],
                "height": upload_result["height"]
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Image upload failed: {str(e)}"
            )

    @staticmethod
    async def delete_image(public_id: str):
        try:
            result = cloudinary.uploader.destroy(public_id)
            if result.get("result") != "ok":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to delete image"
                )
            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Image deletion failed: {str(e)}"
            )