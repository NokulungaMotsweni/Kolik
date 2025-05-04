from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Deletes unverified users older than 24 hours.'

    def handle(self, *args, **kwargs):
        expiration_threshold = timezone.now() - timedelta(hours=24)
        users_to_delete = CustomUser.objects.filter(
            is_active=False,
            date_joined__lt=expiration_threshold
        )
        count = users_to_delete.count()
        users_to_delete.delete()
        self.stdout.write(f"Deleted {count} unverified user(s).")