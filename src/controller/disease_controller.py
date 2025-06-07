from config.config import db
from models.disease_model import Disease
from bson import ObjectId
from datetime import datetime
from typing import List

diseases_collection = db["diseases"]

async def create_disease(disease: Disease) -> Disease:
    disease_data = disease.dict(exclude={"id", "created_at", "updated_at"})
    disease_data["created_at"] = disease_data["updated_at"] = datetime.now()
    
    result = diseases_collection.insert_one(disease_data)
    created_disease = diseases_collection.find_one({"_id": result.inserted_id})
    return Disease(**created_disease)

async def get_disease(id: str) -> Disease:
    disease = diseases_collection.find_one({"_id": ObjectId(id)})
    if disease:
        return Disease(**disease)
    return None

async def get_all_diseases() -> List[Disease]:
    diseases = []
    for disease in diseases_collection.find():
        diseases.append(Disease(**disease))
    return diseases

async def update_disease(id: str, disease: Disease) -> Disease:
    disease_data = disease.dict(exclude={"id", "created_at", "updated_at"})
    disease_data["updated_at"] = datetime.now()
    
    diseases_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": disease_data}
    )
    updated_disease = diseases_collection.find_one({"_id": ObjectId(id)})
    if updated_disease:
        return Disease(**updated_disease)
    return None

async def delete_disease(id: str) -> bool:
    result = diseases_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

async def search_diseases(query: str) -> List[Disease]:
    diseases = []
    regex_query = {"$regex": query, "$options": "i"}
    for disease in diseases_collection.find({
        "$or": [
            {"name": regex_query},
            {"description": regex_query},
            {"symptoms": regex_query}
        ]
    }):
        diseases.append(Disease(**disease))
    return diseases

async def get_disease_count() -> int:
    return diseases_collection.count_documents({})