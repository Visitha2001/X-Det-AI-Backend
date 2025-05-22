# models/gemini_model.py (or modify your existing deepseek_model.py)
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure Gemini with your API key
# It's best practice to store your API key in an environment variable, e.g., GEMINI_API_KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_disease_details_gemini(disease_name: str) -> Optional[str]:
    """
    Get detailed information about a disease from Google Gemini API
    """
    # No explicit API URL needed for google-generativeai client, it's handled internally
    # You might want to specify a model, e.g., "gemini-pro" or "gemini-1.5-flash"
    # Check https://ai.google.dev/models/gemini for available models and their capabilities.
    model = genai.GenerativeModel('gemini-1.5-flash') # Using a common, cost-effective model

    prompt = (
        f"Provide a detailed medical explanation of {disease_name}, including: "
        "1. Definition\n2. Symptoms\n3. Causes\n4. Treatments\n5. Prevention methods\n"
        "Format the response in clear paragraphs with proper headings."
    )

    try:
        # For simple text generation, use generate_content
        response = model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000 # Matches your DeepSeek max_tokens
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Log the error for debugging
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.error(f"Error calling Gemini API: {e}")
        return None