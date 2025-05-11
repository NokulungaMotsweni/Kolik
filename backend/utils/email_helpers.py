from utils.email import send_email
from users.enums import AuditAction
from utils.decorators import log_email_action

@log_email_action(AuditAction.EMAIL_VERIFICATION_SENT)
def send_verification_email(request, user, token):
    """
       Sends a verification email to the user with a link containing a unique token.

       Args:
           request (HttpRequest): The current request object.
           user (User): The user to whom the email is being sent.
           token (str): The email verification token.
       """
    link = f"https://example.com/verify-email/{token}"
    html = f"<p>Click here to verify: <a href='{link}'>Verify</a></p>"
    # Send the Verification Email
    send_email("Verify your email", user.email, html, request=request, user=user)

@log_email_action(AuditAction.PASSWORD_RESET_SENT)
def send_password_reset_email(request, user, token):
    """
        Sends a password reset email to the user with a reset link.

        Args:
            request (HttpRequest): The current request object.
            user (User): The user requesting password reset.
            token (str): The token to identify the password reset request.
        """
    reset_link = f"https://your-frontend-domain.com/reset-password/{token}"
    subject = "Reset your Kolik password"
    html = f"""
            <p>Hello,</p>
            <p>You requested a password reset for your Kolik account. Click below:</p>
            <p><a href='{reset_link}'>Reset My Password</a></p>
            <p>This link will expire in 30 minutes.</p>
            <p>If you didn't request this, ignore this email.</p>
        """
    # Send Password Reset Email
    send_email(subject, user.email, html, request=request, user=user)

@log_email_action(AuditAction.EMAIL_CHANGE_VERIFICATION_SENT)
def send_email_change_verification(request, user, token):
    """
        Sends a confirmation email to verify a requested email change.

        Args:
            request (HttpRequest): The current request object.
            user (User): The user who requested the email change.
            token (str): The token to verify the email change.
        """
    confirmation_link = f"https://your-frontend-domain.com/confirm-email-change/{token}"
    subject = "Confirm Your Kolik Email Change"
    html = f"""
            <p>Hello,</p>
            <p>You requested to change your Kolik email. Confirm it below:</p>
            <p><a href='{confirmation_link}'>Confirm Email Change</a></p>
            <p>This link will expire in 30 minutes.</p>
            <p>If you didn't request this, ignore this email.</p>
        """
    # Send the confirmation email to the pending new email address
    send_email(subject, user.pending_email, html, request=request, user=user)

@log_email_action(AuditAction.PASSWORD_CHANGE_SUCCESS)
def send_password_change_success_email(request, user):
    subject = "Your Kolik Password Has Been Changed"
    html = f"""
        <p>Hello,</p>
        <p>Your Kolik password was changed successfully. If this wasn't you, contact our support team immediately.</p>
        <p>If you recognize this change, you can ignore this email.</p>
    """
    send_email(subject, user.email, html, request=request, user=user)

@log_email_action(AuditAction.EMAIL_CHANGE_SUCCESS)
def send_email_change_success_email(request, user):
    subject = "Your Kolik Email Has Been Successfully Changed"
    html = f"""
        <p>Hello,</p>
        <p>Your Kolik account email address has been successfully changed.</p>
        <p>If this wasn't you, please contact our support team immediately.</p>
    """
    send_email(subject, user.email, html, request=request, user=user)