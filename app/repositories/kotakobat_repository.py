# ------------------------------------------------------------------
# kotakobat_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Kotakobat berdasarkan format data kotakobat yang diatur oleh kotakobat_schema.py
# pada kelas KotakobatCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Kotakobat yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.kotakobat_model import Kotakobat
from app.schemas.kotakobat_schema import KotakobatCreate, KotakobatUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class KotakobatRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data kotakobat
    dengan format data kotakobat sesuai pada kotakobat_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, kotakobat_data: KotakobatCreate):
        kotakobat = Kotakobat(
            id_obat = kotakobat_data.id_obat
        )
        db.add(kotakobat)
        db.commit()
        db.refresh(kotakobat)
        return kotakobat
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel kotakobat yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Kotakobat).all()

    @staticmethod
    def get_by_id(db: Session, kotakobat_id: int):
        return(db.query(Kotakobat).filter(Kotakobat.id == kotakobat_id).first())
    
    @staticmethod
    def update_put(db: Session, kotakobat_id: int, kotakobat_data: KotakobatUpdate):
        kotakobat = db.query(Kotakobat).filter(Kotakobat.id == kotakobat_id).first()

        if not kotakobat:
            return None

        else:
            kotakobat.id_obat = kotakobat_data.id_obat
            kotakobat.updated_at = now()

        db.commit()
        db.refresh(kotakobat)
        return kotakobat
    
    @staticmethod
    def update_patch(db: Session, kotakobat_id:int, payload: dict):
        kotakobat = db.query(Kotakobat).filter(Kotakobat.id == kotakobat_id).first()

        if not kotakobat:
            return None
        
        for key, value in payload.items():

            if not hasattr(Kotakobat, key):
                continue

            setattr(kotakobat, key, value)

        kotakobat.updated_at = now()

        db.commit()
        db.refresh(kotakobat)
        return kotakobat
    
    @staticmethod
    def delete(db: Session, kotakobat_id: int):
        kotakobat = db.query(Kotakobat).filter(Kotakobat.id == kotakobat_id).first()

        if not kotakobat:
            return None

        db.delete(kotakobat)
        db.commit()
        return kotakobat
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Kotakobat).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Kotakobat deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        kotakobat = db.query(Kotakobat)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Kotakobat, key):
                column = getattr(Kotakobat, key)
                if "secret" in column.info:
                    continue

                kotakobat = kotakobat.filter(column == value)
        
        return kotakobat.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Kotakobat).parse()
        
        if expression is None:
            return []        

        return db.query(Kotakobat).filter(expression).all()