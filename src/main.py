from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src import presentation
from src.config import settings
from src.infrastructure.application import create as application_factory

# Adjust the logging
# -------------------------------
logger.add(
    "".join(
        [
            str(settings.root_dir),
            "/logs/",
            settings.logging.file.lower(),
            ".log",
        ]
    ),
    format=settings.logging.format,
    rotation=settings.logging.rotation,
    compression=settings.logging.compression,
    level="INFO",
)


# Adjust the application
# -------------------------------
app: FastAPI = application_factory(
    debug=settings.debug,
    rest_routers=(
        presentation.health.rest.router,
        presentation.authentication.rest.router,
        presentation.users.rest.router,
        presentation.registry.rest.router,
        presentation.models.rest.router,
        # presentation.products.rest.router,    # Architechure test endpoints.
        # presentation.orders.rest.router,      # Architechure test endpoints.
    ),
    startup_tasks=[],
    shutdown_tasks=[],
    startup_processes=[],
    swagger_ui_parameters={"defaultModelsExpandDepth": 1},
    docs_url=settings.public_api.urls.docs,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
