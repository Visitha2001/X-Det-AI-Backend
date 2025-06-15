from fastapi import HTTPException
from models.review import Review
from config.config import db
from bson import ObjectId
from datetime import datetime

reviews_collection = db["reviews"]

def create_review(review: Review):
    review_dict = review.dict()
    result = reviews_collection.insert_one(review_dict)
    return {"id": str(result.inserted_id), **review_dict}

def get_all_reviews():
    reviews = list(reviews_collection.find())
    for review in reviews:
        review["_id"] = str(review["_id"])
    return reviews

def get_reviews_by_username(username: str):
    reviews = list(reviews_collection.find({"username": username}))
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews found for username: {username}")
    for review in reviews:
        review["_id"] = str(review["_id"])
    return reviews

def delete_reviews_by_username(username: str):
    result = reviews_collection.delete_many({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No reviews found for username: {username}")
    return {"message": f"Successfully deleted {result.deleted_count} reviews for username: {username}"}