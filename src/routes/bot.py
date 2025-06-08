from fastapi import APIRouter, HTTPException
from models.chat import (
    DiseaseQuestionsResponse,
    ChatbotQueryRequest,
    ChatbotResponse
)
from controller.ai_chatbot import AIChatbotController

router = APIRouter()
controller = AIChatbotController()

@router.get("/diseases/{disease_name}/suggested-questions", response_model=DiseaseQuestionsResponse)
async def get_suggested_questions(disease_name: str):
    questions = controller.get_suggested_questions(disease_name)
    if not questions:
        raise HTTPException(status_code=404, detail="Disease not found")
    return {"disease": disease_name, "questions": questions}

@router.post("/chat", response_model=ChatbotResponse)
async def chat_with_bot(request: ChatbotQueryRequest):
    response = controller.get_ai_response(request.disease, request.query)
    return {
        "disease": request.disease,
        "question": request.query,
        "answer": response["answer"],
        "confidence": response["confidence"],
        "followup_questions": response["suggested_questions"]
    }