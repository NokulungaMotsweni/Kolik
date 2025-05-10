import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, to_email, html_content, request=None, user=None):
    message = Mail(
        from_email=os.getenv('DEFAULT_FROM_EMAIL'),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print("SendGrid error:", e)
        return None

