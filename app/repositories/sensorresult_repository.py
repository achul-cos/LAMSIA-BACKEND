# ------------------------------------------------------------------
# sensorresult_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Sensorresult berdasarkan format data sensorresult yang diatur oleh sensorresult_schema.py
# pada kelas SensorresultCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Sensorresult yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.sensorresult_model import Sensorresult
from app.schemas.sensorresult_schema import SensorresultCreate, SensorresultUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class SensorresultRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data sensorresult
    dengan format data sensorresult sesuai pada sensorresult_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, sensorresult_data: SensorresultCreate):
        sensorresult = Sensorresult(
            heart_rate = sensorresult_data.heart_rate,
            blood_saturation = sensorresult_data.blood_saturation
        )
        db.add(sensorresult)
        db.commit()
        db.refresh(sensorresult)
        return sensorresult
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel sensorresult yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Sensorresult).all()

    @staticmethod
    def get_by_id(db: Session, sensorresult_id: int):
        return(db.query(Sensorresult).filter(Sensorresult.id == sensorresult_id).first())
    
    @staticmethod
    def update_put(db: Session, sensorresult_id: int, sensorresult_data: SensorresultUpdate):
        sensorresult = db.query(Sensorresult).filter(Sensorresult.id == sensorresult_id).first()

        if not sensorresult:
            return None

        else:
            sensorresult.heart_rate = sensorresult_data.heart_rate
            sensorresult.blood_saturation = sensorresult_data.blood_saturation
            sensorresult.updated_at = now()

        db.commit()
        db.refresh(sensorresult)
        return sensorresult
    
    @staticmethod
    def update_patch(db: Session, sensorresult_id:int, payload: dict):
        sensorresult = db.query(Sensorresult).filter(Sensorresult.id == sensorresult_id).first()

        if not sensorresult:
            return None
        
        for key, value in payload.items():

            if not hasattr(Sensorresult, key):
                continue

            setattr(sensorresult, key, value)

        sensorresult.updated_at = now()

        db.commit()
        db.refresh(sensorresult)
        return sensorresult
    
    @staticmethod
    def delete(db: Session, sensorresult_id: int):
        sensorresult = db.query(Sensorresult).filter(Sensorresult.id == sensorresult_id).first()

        if not sensorresult:
            return None

        db.delete(sensorresult)
        db.commit()
        return sensorresult
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Sensorresult).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Sensorresult deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        sensorresult = db.query(Sensorresult)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Sensorresult, key):
                column = getattr(Sensorresult, key)
                if "secret" in column.info:
                    continue

                sensorresult = sensorresult.filter(column == value)
        
        return sensorresult.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Sensorresult).parse()
        
        if expression is None:
            return []        

        return db.query(Sensorresult).filter(expression).all()