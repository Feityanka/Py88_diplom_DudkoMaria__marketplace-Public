import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTING_MODULE", "Pixel.settings")

app = Celery("Pixel")

#here we are setting our settings.py as default config for celery
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
