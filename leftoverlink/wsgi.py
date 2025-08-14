"""
WSGI config for leftoverlink project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leftoverlink.settings")

application = get_wsgi_application()

# Ensure STATIC_ROOT is correct
BASE_DIR = Path(__file__).resolve().parent.parent
application = WhiteNoise(application, root=BASE_DIR / "staticfiles")
