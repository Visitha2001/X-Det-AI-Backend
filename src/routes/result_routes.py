from fastapi import APIRouter, Depends
from controller.results_controller import create_result
from controller.auth import get_current_user
from models.result_model import ResultCreate
from models.user import User

router = APIRouter()

@router.post("/save-result", response_model=ResultCreate)
def save_result(
    result: ResultCreate, 
    current_user: User = Depends(get_current_user)
):
    return create_result(result, current_user)

@router.get("/results/{username}", response_model=list[ResultCreate])
def get_results(
    username: str,
    current_user: User = Depends(get_current_user)
):
    return get_user_results(username, current_user)