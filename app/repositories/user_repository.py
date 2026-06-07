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
from app.helper.query_parser import QueryParser
from app.core.time import now

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

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return(db.query(User).filter(User.id == user_id).first())
    
    @staticmethod
    def update_put(db: Session, user_id: int, user_data: UserCreate):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None
        
        user.username = user_data.username
        user.telephone = user_data.telephone
        user.password = user_data.password
        user.updated_at = now()

        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_patch(db: Session, user_id:int, payload: dict):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None
        
        for key, value in payload.items():

            if not hasattr(User, key):
                continue

            setattr(user, key, value)

        user.updated_at = now()

        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None
        
            # return({
            #     f"message": "ERROR : user {user_id} not found"
            # })

        db.delete(user)
        db.commit()
        return user
    
    @staticmethod
    def delete_all(db: Session):
        db.query(User).delete(synchronize_session=False)

        db.commit()

        # Reset Auto Increment For SQLite
        # db.execute(f"DELETE FROM sqlite_sequence WHERE name='{User.__tablename__}")

        # Reset Auto Increment For MYSQL
        # db.execute(f"ALTER TABLE {User.__tablename__} AUTO_INCREMENT = 1;")

        # Reset Auto Increment For PostgreSQL
        # db.execute(f"ALTER SEQUENCE {User.__tablename__}_id_seq RESTART WITH 1;")
        
        return {
            "message": f"All {User.__tablename__} deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        user = db.query(User)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(User, key):
                column = getattr(User, key)
                if "secret" in column.info:
                    continue

                user = user.filter(column == value)
        
        return user.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, User).parse()
        
        if expression is None:
            return []        

        return db.query(User).filter(expression).all()