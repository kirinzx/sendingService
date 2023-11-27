import os

from celery import Celery
from celery.schedules import crontab
from celery.app import trace
from celery.worker import strategy
import logging
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

trace.logger.setLevel(logging.WARNING)
strategy.logger.setLevel(logging.WARNING)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'your-task-name': {
        'task': 'apps.sending.tasks.send_info_to_email',
        'schedule': crontab(hour=23, minute=00),
    },
}