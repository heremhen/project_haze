from chromadb.config import Settings

from src.config import settings

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    persist_directory=settings.chroma.persist_directory,
    anonymized_telemetry=settings.chroma.anonymized_telemetry,
)
