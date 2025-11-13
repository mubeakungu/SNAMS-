from celery import Celery
from decouple import config

# 1. Message Broker URL (Required)
# Redis is a fast, common choice for the broker in dev/prod.
# RabbitMQ is the most feature-rich/robust option.
# BROKER_URL is read from the .env file.
BROKER_URL = config("CELERY_BROKER_URL", default="redis://localhost:6379/0")

# 2. Result Backend URL (Optional, but required to track job status/results)
# We use Redis here too, but you could use a dedicated column in Postgres.
BACKEND_URL = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/1")

# 3. Initialize Celery App
celery_app = Celery(
    'snams_tasks',  # Name of the Celery application
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=['app.tasks.net_automation'] # Tells Celery where to find tasks
)

# Optional: Configuration for time zones, enabling the scheduler, etc.
celery_app.conf.update(
    enable_utc=True,
    timezone='UTC',
    result_expires=3600,  # Results expire after 1 hour
    task_track_started=True # Allows tracking status as 'STARTED'
)
