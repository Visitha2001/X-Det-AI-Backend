from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from pathlib import Path

class DiseaseChatModel:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_embeddings = {}
        self.disease_data = {}
        self._load_data()
        self._precompute_embeddings()
    
    def _load_data(self):
        data_path = Path(__file__).parent.parent / "data" / "chest_xray_qa.json"
        with open(data_path, 'r') as f:
            self.disease_data = json.load(f)["diseases"]
    
    def _precompute_embeddings(self):
        for disease, qa_pairs in self.disease_data.items():
            questions = [qa["question"] for qa in qa_pairs]
            self.qa_embeddings[disease] = {
                "questions": questions,
                "embeddings": self.model.encode(questions),
                "answers": [qa["answer"] for qa in qa_pairs]
            }
    
    def find_most_relevant_answer(self, disease: str, query: str, threshold=0.5):
        if disease not in self.qa_embeddings:
            return None
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(
            query_embedding,
            self.qa_embeddings[disease]["embeddings"]
        )[0]
        
        max_idx = np.argmax(similarities)
        if similarities[max_idx] < threshold:
            return None
        
        return {
            "question": self.qa_embeddings[disease]["questions"][max_idx],
            "answer": self.qa_embeddings[disease]["answers"][max_idx],
            "confidence": float(similarities[max_idx])
        }
    
    def generate_smart_response(self, disease: str, query: str):
        # First try to find exact match
        exact_match = self.find_most_relevant_answer(disease, query, threshold=0.7)
        if exact_match:
            return exact_match
        
        # If no good match, use a generative approach (could integrate with LLM)
        general_info = self.disease_data[disease][0]["answer"]
        return {
            "question": query,
            "answer": f"I don't have a specific answer for that, but here's general information about {disease}: {general_info}",
            "confidence": 0.3
        }