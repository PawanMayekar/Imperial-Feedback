"""
Celery application for the sdcorp project.

Start the worker + beat scheduler together on Windows:
    celery -A sdcorp worker --beat --loglevel=info --pool=solo
"""

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdcorp.settings")

app = Celery("sdcorp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "daily-feedback-report": {
        "task": "feedback.tasks.send_feedback_report",
        "schedule": crontab(hour=8, minute=0),
        "kwargs": {"period": "daily"},
    },
}
