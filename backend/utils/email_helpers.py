from utils.email import send_email
from users.enums import AuditAction
from utils.decorators import log_email_action

@log_email_action(AuditAction.EMAIL_VERIFICATION_SENT)
def send_verification_email(request, user, token):
    link = f"https://example.com/verify-email/{token}"
    html = f"<p>Click here to verify: <a href='{link}'>Verify</a></p>"
    send_email("Verify your email", user.email, html, request=request, user=user)

@log_email_action(AuditAction.PASSWORD_RESET_SENT)
def send_password_reset_email(request, user, token):
    reset_link = f"https://your-frontend-domain.com/reset-password/{token}"
    subject = "Reset your Kolik password"
    html = f"""
            <p>Hello,</p>
            <p>You requested a password reset for your Kolik account. Click below:</p>
            <p><a href='{reset_link}'>Reset My Password</a></p>
            <p>This link will expire in 30 minutes.</p>
            <p>If you didn't request this, ignore this email.</p>
        """
    send_email(subject, user.email, html, request=request, user=user)

@log_email_action(AuditAction.EMAIL_CHANGE_VERIFICATION_SENT)
def send_email_change_verification(request, user, token):
    confirmation_link = f"https://your-frontend-domain.com/confirm-email-change/{token}"
    subject = "Confirm Your Kolik Email Change"
    html = f"""
            <p>Hello,</p>
            <p>You requested to change your Kolik email. Confirm it below:</p>
            <p><a href='{confirmation_link}'>Confirm Email Change</a></p>
            <p>This link will expire in 30 minutes.</p>
            <p>If you didn't request this, ignore this email.</p>
        """
    send_email(subject, user.pending_email, html, request=request, user=user)