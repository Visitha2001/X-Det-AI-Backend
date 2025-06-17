import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your Gmail or Mailtrap SMTP info
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "ruwanmg99@gmail.com"
SMTP_PASSWORD = "mwiy jsia jmpx pfjn"
FROM_EMAIL = SMTP_USERNAME

def send_email(to: str, subject: str, body: str, html_body: str = None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to

    # Plain-text fallback
    part1 = MIMEText(body, "plain")
    msg.attach(part1)

    # HTML content (optional)
    if html_body:
        part2 = MIMEText(html_body, "html")
        msg.attach(part2)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Error sending email:", e)