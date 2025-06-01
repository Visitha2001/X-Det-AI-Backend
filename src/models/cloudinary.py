from pydantic_settings import BaseSettings

class CloudinarySettings(BaseSettings):
    cloud_name: str
    api_key: str
    api_secret: str

    class Config:
        env_prefix = "CLOUDINARY_"
        env_file = ".env"