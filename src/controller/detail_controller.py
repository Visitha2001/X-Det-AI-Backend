# controller/detail_controller.py
from typing import Dict
from fastapi import HTTPException
# from models.deepseek_model import get_disease_details # Remove or comment out
from models.gemini_model import get_disease_details_gemini # Import the new function
import logging

logger = logging.getLogger(__name__)

def generate_disease_details(disease_name: str) -> Dict[str, str]:
    """
    Generate detailed information about a disease using Gemini API
    """
    if not disease_name or disease_name.strip() == "":
        raise HTTPException(status_code=400, detail="Disease name cannot be empty")
    
    try:
        # Change this line to call the Gemini function
        details = get_disease_details_gemini(disease_name)
        
        if not details:
            raise HTTPException(
                status_code=502,
                detail="Failed to generate disease details from the AI service."
            )
        
        return {
            "disease": disease_name,
            "details": details
        }
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error. Please contact administrator."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )