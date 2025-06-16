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
    formatted_reviews = []
    for review in reviews:
        review["id"] = str(review["_id"])
        del review["_id"]
        formatted_reviews.append(review)
    return formatted_reviews

def get_reviews_by_username(username: str):
    reviews = list(reviews_collection.find({"username": username}))
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews found for username: {username}")
    formatted_reviews = []
    for review in reviews:
        review["id"] = str(review["_id"])
        del review["_id"]
        formatted_reviews.append(review)
    
    return formatted_reviews

def delete_reviews_by_username(username: str):
    result = reviews_collection.delete_many({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No reviews found for username: {username}")
    return {"message": f"Successfully deleted {result.deleted_count} reviews for username: {username}"}

def delete_review_by_id(review_id: str):
    try:
        result = reviews_collection.delete_one({"_id": ObjectId(review_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"No review found with id: {review_id}")
        return {"message": f"Successfully deleted review with id: {review_id}"}
    except:
        raise HTTPException(status_code=400, detail=f"Invalid review id: {review_id}")

def delete_review_by_username_and_id(username: str, review_id: str):
    try:
        result = reviews_collection.delete_one({
            "_id": ObjectId(review_id),
            "username": username
        })
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"No review found with id: {review_id} for username: {username}"
            )
        return {"message": f"Successfully deleted review with id: {review_id} for username: {username}"}
    except:
        raise HTTPException(status_code=400, detail=f"Invalid review id: {review_id}")