from fastapi import APIRouter, HTTPException, Query
from controller.disease_controller import (
    create_disease,
    get_disease,
    get_all_diseases,
    update_disease,
    delete_disease,
    search_diseases
)
from models.disease_model import Disease
from typing import List

router = APIRouter(
    prefix="/diseases",
    tags=["diseases"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Disease)
async def create_disease_route(disease: Disease):
    return await create_disease(disease)

@router.get("/", response_model=List[Disease])
async def get_all_diseases_route():
    return await get_all_diseases()

@router.get("/{disease_id}", response_model=Disease)
async def get_disease_route(disease_id: str):
    disease = await get_disease(disease_id)
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@router.put("/{id}", response_model=Disease)
async def update_disease_route(id: str, disease: Disease):
    updated_disease = await update_disease(id, disease)
    if not updated_disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return updated_disease

@router.delete("/{id}")
async def delete_disease_route(id: str):
    if not await delete_disease(id):
        raise HTTPException(status_code=404, detail="Disease not found")
    return {"message": "Disease deleted successfully"}

@router.get("/search/", response_model=List[Disease])
async def search_diseases_route(query: str = Query(..., min_length=1)):
    return await search_diseases(query)