from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIUrlsSettings(BaseModel):
    """API public urls settings."""

    docs: str = "/"
    redoc: str = "/redoc"


class PublicApiSettings(BaseModel):
    """Configure public API service settings."""

    name: str = "SAKANAYA_GOHAN"
    urls: APIUrlsSettings = APIUrlsSettings()


class DatabaseSettings(BaseModel):
    name: str = "db.sqlite3"

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///./{self.name}"


class LoggingSettings(BaseModel):
    """Configure the logging engine."""

    # The time field can be formatted using more human-friendly tokens.
    # These constitute a subset of the one used by the Pendulum library
    # https://pendulum.eustace.io/docs/#tokens
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}"

    # The .log filename
    file: str = "CH4NGE"

    # The .log file Rotation
    rotation: str = "10MB"

    # The type of compression
    compression: str = "zip"


class AccessTokenSettings(BaseModel):
    secret_key: str = "invaliad"
    ttl: int = 100  # seconds


class RefreshTokenSettings(BaseModel):
    secret_key: str = "invaliad"
    ttl: int = 100  # seconds


class AuthenticationSettings(BaseModel):
    access_token: AccessTokenSettings = AccessTokenSettings()
    refresh_token: RefreshTokenSettings = RefreshTokenSettings()
    algorithm: str = "HS256"
    scheme: str = "Bearer"


class CelerySettings(BaseModel):
    """Configure celery redis settings."""

    broker_url: str = ""
    result_backend: str = ""


# Define the root path
# --------------------------------------
ROOT_PATH = Path(__file__).parent.parent.parent


class ChromaSettings(BaseModel):
    """Configure chroma base settings."""

    persist_directory: str = f"{ROOT_PATH}/static/chroma"
    anonymized_telemetry: bool = False
    source_directory: str = f"{ROOT_PATH}/static/source_documents"
    chunk_size: int = 500
    chunk_overlap: int = 50
    target_source_chunks: int = 4
    model: str = "mistral"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=ROOT_PATH / ".env", extra="ignore"
    )

    # Infrastructure settings
    database: DatabaseSettings = DatabaseSettings()
    celery: CelerySettings = CelerySettings()
    chroma: ChromaSettings = ChromaSettings()

    # Application configuration
    root_dir: Path
    src_dir: Path
    debug: bool = True
    public_api: PublicApiSettings = PublicApiSettings()
    logging: LoggingSettings = LoggingSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()


# ======================================
# Load settings
# ======================================
settings = Settings(
    # NOTE: We would like to hard-code the root and applications directories
    #       to avoid overriding via environment variables
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)
