import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_STARTTLS = os.getenv("MAIL_STARTTLS") 
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS") 
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,   
    MAIL_STARTTLS=MAIL_STARTTLS,   
    MAIL_SSL_TLS=MAIL_SSL_TLS, 
    USE_CREDENTIALS=True
)

fast_mail = FastMail(conf)

async def send_ticket_update_email(ticket):
    """Sends an email notification when a ticket is updated."""
    email_subject = f"Your Ticket #{ticket.id} Status Updated"
    email_body = f"""
    Hello {ticket.name},

    Your ticket regarding "{ticket.title}" has been updated.
    
    New Status: {ticket.status.value}

    Thank you for using our support system.

    Regards,
    Support Team
    """

    message = MessageSchema(
        subject=email_subject,
        recipients=[ticket.email],  
        body=email_body,
        subtype="plain"
    )

    await fast_mail.send_message(message)  
