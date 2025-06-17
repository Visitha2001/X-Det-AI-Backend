from fastapi import APIRouter
from models.subscriber_model import Subscriber, EmailRequest
from controller.subscriber_controller import subscribe_user, send_custom_email_to_all, get_all_subscribers

router = APIRouter()

@router.post("/subscribe")
def subscribe(subscriber: Subscriber):
    return subscribe_user(subscriber)

@router.post("/send-newsletter")
def send_newsletter(email_data: EmailRequest):
    return send_custom_email_to_all(email_data)

@router.get("/subscribers")
def list_subscribers():
    return get_all_subscribers()