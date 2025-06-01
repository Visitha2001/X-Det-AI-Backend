from fastapi import HTTPException, Depends
from models.result_model import ResultCreate
from config.config import db
from controller.auth import get_current_user
from models.user import User

results_collection = db["results"]

def create_result(result: ResultCreate, current_user: User = Depends(get_current_user)):
    try:
        # Ensure the username in the result matches the authenticated user
        if result.username != current_user.username:
            raise HTTPException(status_code=403, detail="Not authorized to save results for this user")
            
        result_dict = result.dict()
        # Convert datetime to proper format for MongoDB
        result_dict['timestamp'] = result_dict['timestamp'].isoformat()
        results_collection.insert_one(result_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save result: {str(e)}")

def get_user_results(username: str, current_user: User = Depends(get_current_user)):
    try:
        # Ensure the requested username matches the authenticated user
        if username != current_user.username:
            raise HTTPException(status_code=403, detail="Not authorized to view these results")
            
        results = list(results_collection.find({"username": username}))
        # Convert MongoDB _id to string for JSON serialization
        for result in results:
            result['_id'] = str(result['_id'])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch results: {str(e)}")