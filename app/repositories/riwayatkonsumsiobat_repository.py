# ------------------------------------------------------------------
# riwayatkonsumsiobat_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Riwayatkonsumsiobat berdasarkan format data riwayatkonsumsiobat yang diatur oleh riwayatkonsumsiobat_schema.py
# pada kelas RiwayatkonsumsiobatCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Riwayatkonsumsiobat yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.riwayatkonsumsiobat_model import Riwayatkonsumsiobat
from app.schemas.riwayatkonsumsiobat_schema import RiwayatkonsumsiobatCreate, RiwayatkonsumsiobatUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class RiwayatkonsumsiobatRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data riwayatkonsumsiobat
    dengan format data riwayatkonsumsiobat sesuai pada riwayatkonsumsiobat_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, riwayatkonsumsiobat_data: RiwayatkonsumsiobatCreate):
        riwayatkonsumsiobat = Riwayatkonsumsiobat(
            kompartemen = riwayatkonsumsiobat_data.kompartemen,
            waktu_minum = riwayatkonsumsiobat_data.waktu_minum
        )
        db.add(riwayatkonsumsiobat)
        db.commit()
        db.refresh(riwayatkonsumsiobat)
        return riwayatkonsumsiobat
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel riwayatkonsumsiobat yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Riwayatkonsumsiobat).all()

    @staticmethod
    def get_by_id(db: Session, riwayatkonsumsiobat_id: int):
        return(db.query(Riwayatkonsumsiobat).filter(Riwayatkonsumsiobat.id == riwayatkonsumsiobat_id).first())
    
    @staticmethod
    def update_put(db: Session, riwayatkonsumsiobat_id: int, riwayatkonsumsiobat_data: RiwayatkonsumsiobatUpdate):
        riwayatkonsumsiobat = db.query(Riwayatkonsumsiobat).filter(Riwayatkonsumsiobat.id == riwayatkonsumsiobat_id).first()

        if not riwayatkonsumsiobat:
            return None

        else:
            riwayatkonsumsiobat.kompartemen = riwayatkonsumsiobat_data.kompartemen
            riwayatkonsumsiobat.waktu_minum = riwayatkonsumsiobat_data.waktu_minum
            riwayatkonsumsiobat.waktu_balikin = riwayatkonsumsiobat_data.waktu_balikin
            riwayatkonsumsiobat.updated_at = now()

        db.commit()
        db.refresh(riwayatkonsumsiobat)
        return riwayatkonsumsiobat
    
    @staticmethod
    def update_patch(db: Session, riwayatkonsumsiobat_id:int, payload: dict):
        riwayatkonsumsiobat = db.query(Riwayatkonsumsiobat).filter(Riwayatkonsumsiobat.id == riwayatkonsumsiobat_id).first()

        if not riwayatkonsumsiobat:
            return None
        
        for key, value in payload.items():

            if not hasattr(Riwayatkonsumsiobat, key):
                continue

            setattr(riwayatkonsumsiobat, key, value)

        riwayatkonsumsiobat.updated_at = now()

        db.commit()
        db.refresh(riwayatkonsumsiobat)
        return riwayatkonsumsiobat
    
    @staticmethod
    def delete(db: Session, riwayatkonsumsiobat_id: int):
        riwayatkonsumsiobat = db.query(Riwayatkonsumsiobat).filter(Riwayatkonsumsiobat.id == riwayatkonsumsiobat_id).first()

        if not riwayatkonsumsiobat:
            return None

        db.delete(riwayatkonsumsiobat)
        db.commit()
        return riwayatkonsumsiobat
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Riwayatkonsumsiobat).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Riwayatkonsumsiobat deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        riwayatkonsumsiobat = db.query(Riwayatkonsumsiobat)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Riwayatkonsumsiobat, key):
                column = getattr(Riwayatkonsumsiobat, key)
                if "secret" in column.info:
                    continue

                riwayatkonsumsiobat = riwayatkonsumsiobat.filter(column == value)
        
        return riwayatkonsumsiobat.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Riwayatkonsumsiobat).parse()
        
        if expression is None:
            return []        

        return db.query(Riwayatkonsumsiobat).filter(expression).all()