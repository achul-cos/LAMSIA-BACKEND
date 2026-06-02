from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Migration(Base):
    __tablename__ = "migrations"
    id = Column(Integer, primary_key=True)
    migration_name = Column(
        String(255),
        nullable=False,
        unique=True
    )