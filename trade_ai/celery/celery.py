from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('trade_ai', broker="redis://localhost:6379/0")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='celery' means all celery-related configuration keys
#   should have a `celery_` prefix.
app.config_from_object('django.conf:settings')
app.conf.task_create_missing_queues = True
# Load task modules from all registered Django app configs.


app.autodiscover_tasks(settings.INSTALLED_APPS)
