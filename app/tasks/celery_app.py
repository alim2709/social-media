import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env-non-dev')

celery = Celery(
    "social-media-app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=['app.tasks.tasks']
)
