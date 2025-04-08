# WSGI config — used only in production (e.g. Render.com).
# You don't need to modify this during development.

import os
from django.core.wsgi import get_wsgi_application

# Tell Django which settings file to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Get the WSGI application for use by production servers
application = get_wsgi_application()