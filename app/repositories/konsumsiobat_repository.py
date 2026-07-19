# ------------------------------------------------------------------
# konsumsiobat_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Konsumsiobat berdasarkan format data konsumsiobat yang diatur oleh konsumsiobat_schema.py
# pada kelas KonsumsiobatCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Konsumsiobat yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.konsumsiobat_model import Konsumsiobat
from app.schemas.konsumsiobat_schema import KonsumsiobatCreate, KonsumsiobatUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class KonsumsiobatRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data konsumsiobat
    dengan format data konsumsiobat sesuai pada konsumsiobat_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, konsumsiobat_data: KonsumsiobatCreate):
        konsumsiobat = Konsumsiobat(
            id_obat = konsumsiobat_data.id_obat,
            id_kotakobat = konsumsiobat_data.id_kotakobat,
            waktu_minum = konsumsiobat_data.waktu_minum
        )
        db.add(konsumsiobat)
        db.commit()
        db.refresh(konsumsiobat)
        return konsumsiobat
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel konsumsiobat yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Konsumsiobat).all()

    @staticmethod
    def get_by_id(db: Session, konsumsiobat_id: int):
        return(db.query(Konsumsiobat).filter(Konsumsiobat.id == konsumsiobat_id).first())
    
    @staticmethod
    def update_put(db: Session, konsumsiobat_id: int, konsumsiobat_data: KonsumsiobatUpdate):
        konsumsiobat = db.query(Konsumsiobat).filter(Konsumsiobat.id == konsumsiobat_id).first()

        if not konsumsiobat:
            return None

        else:
            konsumsiobat.id_obat = konsumsiobat_data.id_obat
            konsumsiobat.id_kotakobat = konsumsiobat_data.id_kotakobat
            konsumsiobat.waktu_minum = konsumsiobat_data.waktu_minum
            konsumsiobat.waktu_balikin = konsumsiobat_data.waktu_balikin
            konsumsiobat.updated_at = now()

        db.commit()
        db.refresh(konsumsiobat)
        return konsumsiobat
    
    @staticmethod
    def update_patch(db: Session, konsumsiobat_id:int, payload: dict):
        konsumsiobat = db.query(Konsumsiobat).filter(Konsumsiobat.id == konsumsiobat_id).first()

        if not konsumsiobat:
            return None
        
        for key, value in payload.items():

            if not hasattr(Konsumsiobat, key):
                continue

            setattr(konsumsiobat, key, value)

        konsumsiobat.updated_at = now()

        db.commit()
        db.refresh(konsumsiobat)
        return konsumsiobat
    
    @staticmethod
    def delete(db: Session, konsumsiobat_id: int):
        konsumsiobat = db.query(Konsumsiobat).filter(Konsumsiobat.id == konsumsiobat_id).first()

        if not konsumsiobat:
            return None

        db.delete(konsumsiobat)
        db.commit()
        return konsumsiobat
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Konsumsiobat).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Konsumsiobat deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        konsumsiobat = db.query(Konsumsiobat)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Konsumsiobat, key):
                column = getattr(Konsumsiobat, key)
                if "secret" in column.info:
                    continue

                konsumsiobat = konsumsiobat.filter(column == value)
        
        return konsumsiobat.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Konsumsiobat).parse()
        
        if expression is None:
            return []        

        return db.query(Konsumsiobat).filter(expression).all()