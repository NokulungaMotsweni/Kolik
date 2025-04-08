# ASGI config — used for async features (WebSockets, live updates, etc.)
# Not needed now, but included for future compatibility and deployment

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
