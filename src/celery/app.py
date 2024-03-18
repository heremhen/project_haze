from celery import Celery

from src.config import settings

celery_app = Celery(
    broker_url=settings.celery.broker_url,
    result_backend=settings.celery.result_backend,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    include=[
        "src.celery.worker",
        "src.application.models.pipeline_utils",
        "src.application.foxtail.ingest",
        "src.application.foxtail.privateGPT",
    ],
    broker_transport_options={
        "max_retries": 1,
        "visibility_timeout": 365 * 24 * 60 * 60,
        "broker_connection_retry_on_startup": True,
    },
)
