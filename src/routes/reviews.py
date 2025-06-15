from fastapi import APIRouter
from models.review import Review
from controller.reviews_controller import (
    create_review,
    get_all_reviews,
    get_reviews_by_username,
    delete_reviews_by_username
)

router = APIRouter()

@router.post("/reviews", response_model=Review)
async def create_new_review(review: Review):
    return create_review(review)

@router.get("/reviews", response_model=list[Review])
async def get_all_reviews_endpoint():
    return get_all_reviews()

@router.get("/reviews/{username}", response_model=list[Review])
async def get_reviews_by_username_endpoint(username: str):
    return get_reviews_by_username(username)

@router.delete("/reviews/{username}")
async def delete_reviews_by_username_endpoint(username: str):
    return delete_reviews_by_username(username)