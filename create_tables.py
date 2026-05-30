from app.core.database import engine, Base
from app.models.user_model import User

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")