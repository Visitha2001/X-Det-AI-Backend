from pydantic import BaseModel
from typing import List, Optional

class DiseaseQuestionsResponse(BaseModel):
    disease: str
    questions: List[str]

class ChatbotQueryRequest(BaseModel):
    disease: str
    query: str

class ChatbotResponse(BaseModel):
    disease: str
    question: str
    answer: str
    confidence: float
    followup_questions: List[str]