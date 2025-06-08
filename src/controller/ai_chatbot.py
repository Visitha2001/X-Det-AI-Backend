from models.nlp_model import DiseaseChatModel
from typing import List, Optional, Dict

class AIChatbotController:
    def __init__(self):
        self.model = DiseaseChatModel()
    
    def get_suggested_questions(self, disease: str) -> List[str]:
        """Get relevant questions for a disease"""
        if disease not in self.model.disease_data:
            return []
        return [qa["question"] for qa in self.model.disease_data[disease][:15]]
    
    def get_ai_response(self, disease: str, query: str) -> Dict:
        """Get AI-generated response for a query"""
        if disease not in self.model.disease_data:
            return {
                "answer": f"I don't have information about {disease}. Please select from available diseases.",
                "confidence": 0.0
            }
        
        response = self.model.generate_smart_response(disease, query)
        return {
            "disease": disease,
            "question": query,
            "answer": response["answer"],
            "confidence": response["confidence"],
            "suggested_questions": self.get_suggested_questions(disease)
        }