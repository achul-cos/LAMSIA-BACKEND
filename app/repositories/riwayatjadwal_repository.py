# ------------------------------------------------------------------
# riwayatjadwal_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Riwayatjadwal berdasarkan format data riwayatjadwal yang diatur oleh riwayatjadwal_schema.py
# pada kelas RiwayatjadwalCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Riwayatjadwal yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.riwayatjadwal_model import Riwayatjadwal
from app.schemas.riwayatjadwal_schema import RiwayatjadwalCreate, RiwayatjadwalUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class RiwayatjadwalRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data riwayatjadwal
    dengan format data riwayatjadwal sesuai pada riwayatjadwal_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, riwayatjadwal_data: RiwayatjadwalCreate):
        riwayatjadwal = Riwayatjadwal(
            id_jadwal = riwayatjadwal_data.id_jadwal,
            waktu_riwayat = riwayatjadwal_data.waktu_riwayat
        )
        db.add(riwayatjadwal)
        db.commit()
        db.refresh(riwayatjadwal)
        return riwayatjadwal
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel riwayatjadwal yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Riwayatjadwal).all()

    @staticmethod
    def get_by_id(db: Session, riwayatjadwal_id: int):
        return(db.query(Riwayatjadwal).filter(Riwayatjadwal.id == riwayatjadwal_id).first())
    
    @staticmethod
    def update_put(db: Session, riwayatjadwal_id: int, riwayatjadwal_data: RiwayatjadwalUpdate):
        riwayatjadwal = db.query(Riwayatjadwal).filter(Riwayatjadwal.id == riwayatjadwal_id).first()

        if not riwayatjadwal:
            return None

        else:
            riwayatjadwal.id_jadwal = riwayatjadwal_data.id_jadwal
            riwayatjadwal.waktu_riwayat = riwayatjadwal_data.waktu_riwayat
            riwayatjadwal.updated_at = now()

        db.commit()
        db.refresh(riwayatjadwal)
        return riwayatjadwal
    
    @staticmethod
    def update_patch(db: Session, riwayatjadwal_id:int, payload: dict):
        riwayatjadwal = db.query(Riwayatjadwal).filter(Riwayatjadwal.id == riwayatjadwal_id).first()

        if not riwayatjadwal:
            return None
        
        for key, value in payload.items():

            if not hasattr(Riwayatjadwal, key):
                continue

            setattr(riwayatjadwal, key, value)

        riwayatjadwal.updated_at = now()

        db.commit()
        db.refresh(riwayatjadwal)
        return riwayatjadwal
    
    @staticmethod
    def delete(db: Session, riwayatjadwal_id: int):
        riwayatjadwal = db.query(Riwayatjadwal).filter(Riwayatjadwal.id == riwayatjadwal_id).first()

        if not riwayatjadwal:
            return None

        db.delete(riwayatjadwal)
        db.commit()
        return riwayatjadwal
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Riwayatjadwal).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Riwayatjadwal deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        riwayatjadwal = db.query(Riwayatjadwal)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Riwayatjadwal, key):
                column = getattr(Riwayatjadwal, key)
                if "secret" in column.info:
                    continue

                riwayatjadwal = riwayatjadwal.filter(column == value)
        
        return riwayatjadwal.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Riwayatjadwal).parse()
        
        if expression is None:
            return []        

        return db.query(Riwayatjadwal).filter(expression).all()