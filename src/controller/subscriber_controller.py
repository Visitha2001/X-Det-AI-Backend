from fastapi import HTTPException
from mail.mailer import send_email
from models.subscriber_model import Subscriber, EmailRequest
from config.config import db

subscribers_collection = db["subscribers"]

def subscribe_user(subscriber: Subscriber):
    existing = subscribers_collection.find_one({"email": subscriber.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already subscribed")

    subscribers_collection.insert_one(subscriber.dict())
    send_email(
        to=subscriber.email,
        subject="Thank you for subscribing!",
        body=f"Hello {subscriber.username},\n\nThanks for subscribing to X-Det-Ai newsletter!",
        html_body=html_content
    )
    return {"message": "Subscribed successfully and email sent."}

def send_custom_email_to_all(email_data: EmailRequest):
    all_subscribers = subscribers_collection.find()
    count = 0
    for sub in all_subscribers:
        send_email(
            to=sub["email"],
            subject=email_data.subject,
            body=email_data.body
        )
        count += 1
    return {"message": f"Email sent to {count} subscribers."}

html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <div style="max-width: 600px; margin: auto; padding: 20px; background: #f9f9f9; border-radius: 10px;">
      <img src="https://res.cloudinary.com/dqmeeveij/image/upload/v1751270006/Light_Logo_y1wauz.png" alt="Newsletter Banner" style="width: 100%; border-radius: 10px;" />
      <h2 style="color: #333;">Welcome to X-Det-Ai!</h2>
      <p>Thank you for subscribing to X-Det-Ai newsletter. You'll now receive the latest updates and insights from the world of AI-powered diagnostics.</p>
      <p>We're thrilled to have you on board!</p>
      <a href="https://your-website.com" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007BFF; color: white; text-decoration: none; border-radius: 5px;">Visit Website</a>
    </div>
  </body>
</html>
"""

def get_all_subscribers():
    subscribers = list(subscribers_collection.find({}, {"_id": 0}))
    return {"subscribers": subscribers}