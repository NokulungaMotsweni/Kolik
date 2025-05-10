from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from users.models import VerificationType, UserVerification
from utils.email import send_email  # or your wrapped helper
from utils.email_helpers import send_verification_email


@login_required
def test_email_send(request):
    if not settings.DEBUG:
        return HttpResponseForbidden("Not allowed in production.")

    user = request.user

    # Create a real token and verification record
    verification_type, _ = VerificationType.objects.get_or_create(
        name="Email",
        defaults={"requires_token": True, "expires_on": timedelta(minutes=30)}
    )

    verification = UserVerification.objects.create(
        user=user,
        verification_type=verification_type,
        expires_at=timezone.now() + verification_type.expires_on
    )

    raw_token = verification.generate_token()

    # Send it using your helper
    send_verification_email(request, user, raw_token)

    return JsonResponse({
        "email_sent_to": user.email,
        "token": raw_token,
        "expires_at": verification.expires_at
    })