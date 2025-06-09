import os
import google.generativeai as genai
from dotenv import load_dotenv
from models.g_chat_model import MedicalQuery, MedicalResponse, Message

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are a medical information assistant. Respond to health questions with:
1. Clear, factual information
2. No diagnoses or treatment recommendations
3. Always include this disclaimer: "Consult a healthcare professional for personal advice."

If the question isn't medical, respond: "I specialize only in medical questions."
"""

class ChatController:
    @staticmethod
    async def get_medical_answer(query: MedicalQuery) -> MedicalResponse:
        try:
            # Prepare conversation history
            history = query.conversation_history or []
            
            # Format messages for Gemini
            messages = [{"role": "user", "parts": [SYSTEM_PROMPT]}]
            for msg in history:
                messages.append({"role": msg.role, "parts": [msg.content]})
            messages.append({"role": "user", "parts": [query.question]})
            
            # Generate response
            response = await model.generate_content_async(messages)
            
            # Update conversation history
            new_history = history + [
                Message(role="user", content=query.question),
                Message(role="assistant", content=response.text)
            ]
            
            return MedicalResponse(
                answer=response.text,
                conversation_history=new_history
            )
            
        except Exception as e:
            return MedicalResponse(
                answer=f"Error processing your question: {str(e)}",
                conversation_history=query.conversation_history or []
            )