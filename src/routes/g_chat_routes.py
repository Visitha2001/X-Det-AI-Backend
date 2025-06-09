from fastapi import APIRouter
from controller.g_chat_controller import ChatController
from models.g_chat_model import MedicalQuery, MedicalResponse

router = APIRouter()

@router.post("/g_chat", response_model=MedicalResponse)
async def ask_medical(query: MedicalQuery):
    """Endpoint for medical questions with conversation history"""
    return await ChatController.get_medical_answer(query)