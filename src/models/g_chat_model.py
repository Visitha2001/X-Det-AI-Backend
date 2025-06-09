from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class MedicalQuery(BaseModel):
    question: str
    conversation_history: Optional[List[Message]] = None

class MedicalResponse(BaseModel):
    answer: str
    conversation_history: List[Message]
    disclaimer: str = "Note: This is general health information, not medical advice. Consult a healthcare professional for personal concerns."