import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "post_manager.settings")

app = Celery("post_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
