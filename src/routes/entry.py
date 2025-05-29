from fastapi import APIRouter

entry_root = APIRouter()

# endpoints
@entry_root.get("/")
def apiRunning():
    res = {
        "status": "success",
        "code": 200,
        "data": None,
        "message": "API is running."
    }
    return res