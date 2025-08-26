import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_disease_details_gemini(disease_name: str, language: str = "en") -> Optional[str]:
    """
    Get detailed information about a disease from Google Gemini API
    """
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
    # Base prompt in English
    base_prompt = (
        f"Provide a detailed medical explanation of {disease_name}, including: "
        "1. Definition\n2. Symptoms\n3. Causes\n4. Treatments\n5. Prevention methods\n"
        "Format the response in clear paragraphs,points,bold tests,lists,tables with proper headings."
        "at least i need 1000 words"
        "don't mention 'i can explain', 'this description about' in the begining"
    )
    
    # Add language instruction
    if language == "si":
        prompt = base_prompt + "\n\nProvide the response in Sinhala (Sinhala letters only)."
    else:
        prompt = base_prompt + "\n\nProvide the response in English."

    try:
        response = model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=10000
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None