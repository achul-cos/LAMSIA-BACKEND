from pathlib import Path

class Config:

    PROJECT_NAME = "LAMSIA"

    VERSION = "0.1"

    APP_PATH = Path(
        "app"
    )

    MODEL_PATH = (
        APP_PATH / "models"
    )

    SCHEMA_PATH = (
        APP_PATH / "schemas"
    )

    REPOSITORY_PATH = (
        APP_PATH / "repositories"
    )

    ROUTE_PATH = (
        APP_PATH / "routes"
    )

    MIGRATION_PATH = (
        APP_PATH / "migrations/versions"
    )
