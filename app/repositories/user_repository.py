# ------------------------------------------------------------------
# user_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# User berdasarkan format data user yang diatur oleh user_schema.py
# pada kelas UserCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data user yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

class UserRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data user
    dengan format data user sesuai pada user_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, user_data: UserCreate):
        user = User(
            username = user_data.username,
            telephone = user_data.telephone,
            password = user_data.password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel user yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()