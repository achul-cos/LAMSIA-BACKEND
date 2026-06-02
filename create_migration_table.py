from app.core.database import engine
from app.migrations.migration_model import Migration

Migration.__table__.create(
    bind=engine,
    checkfirst=True
)

print("Migration Table Created")