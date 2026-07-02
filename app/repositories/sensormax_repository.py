# ------------------------------------------------------------------
# sensormax_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Sensormax berdasarkan format data sensormax yang diatur oleh sensormax_schema.py
# pada kelas SensormaxCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Sensormax yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.sensormax_model import Sensormax
from app.schemas.sensormax_schema import SensormaxCreate, SensormaxUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class SensormaxRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data sensormax
    dengan format data sensormax sesuai pada sensormax_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, sensormax_data: SensormaxCreate):
        sensormax = Sensormax(
            hr = sensormax_data.hr,
            sp = sensormax_data.sp,
            ir = sensormax_data.ir,
            red = sensormax_data.red
        )
        db.add(sensormax)
        db.commit()
        db.refresh(sensormax)
        return sensormax
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel sensormax yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Sensormax).all()

    @staticmethod
    def get_by_id(db: Session, sensormax_id: int):
        return(db.query(Sensormax).filter(Sensormax.id == sensormax_id).first())
    
    @staticmethod
    def update_put(db: Session, sensormax_id: int, sensormax_data: SensormaxUpdate):
        sensormax = db.query(Sensormax).filter(Sensormax.id == sensormax_id).first()

        if not sensormax:
            return None

        else:
            sensormax.hr = sensormax_data.hr
            sensormax.sp = sensormax_data.sp
            sensormax.ir = sensormax_data.ir
            sensormax.red = sensormax_data.red
            sensormax.updated_at = now()

        db.commit()
        db.refresh(sensormax)
        return sensormax
    
    @staticmethod
    def update_patch(db: Session, sensormax_id:int, payload: dict):
        sensormax = db.query(Sensormax).filter(Sensormax.id == sensormax_id).first()

        if not sensormax:
            return None
        
        for key, value in payload.items():

            if not hasattr(Sensormax, key):
                continue

            setattr(sensormax, key, value)

        sensormax.updated_at = now()

        db.commit()
        db.refresh(sensormax)
        return sensormax
    
    @staticmethod
    def delete(db: Session, sensormax_id: int):
        sensormax = db.query(Sensormax).filter(Sensormax.id == sensormax_id).first()

        if not sensormax:
            return None

        db.delete(sensormax)
        db.commit()
        return sensormax
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Sensormax).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Sensormax deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        sensormax = db.query(Sensormax)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Sensormax, key):
                column = getattr(Sensormax, key)
                if "secret" in column.info:
                    continue

                sensormax = sensormax.filter(column == value)
        
        return sensormax.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Sensormax).parse()
        
        if expression is None:
            return []        

        return db.query(Sensormax).filter(expression).all()