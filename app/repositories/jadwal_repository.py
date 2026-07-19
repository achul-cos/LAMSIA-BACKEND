# ------------------------------------------------------------------
# jadwal_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Jadwal berdasarkan format data jadwal yang diatur oleh jadwal_schema.py
# pada kelas JadwalCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Jadwal yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session, selectinload
from app.models.jadwal_model import Jadwal
from app.schemas.jadwal_schema import JadwalCreate, JadwalUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class JadwalRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data jadwal
    dengan format data jadwal sesuai pada jadwal_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, jadwal_data: JadwalCreate):
        jadwal = Jadwal(
            id_obat = jadwal_data.id_obat,
            dosis = jadwal_data.dosis,
            waktu_minum = jadwal_data.waktu_minum
        )
        db.add(jadwal)
        db.commit()
        db.refresh(jadwal)
        return jadwal
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel jadwal yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Jadwal).options(
            selectinload(Jadwal.riwayatjadwals),
            selectinload(Jadwal.obat),
        ).all()

    @staticmethod
    def get_by_id(db: Session, jadwal_id: int):
        return(db.query(Jadwal).filter(Jadwal.id == jadwal_id).first())
    
    @staticmethod
    def update_put(db: Session, jadwal_id: int, jadwal_data: JadwalUpdate):
        jadwal = db.query(Jadwal).filter(Jadwal.id == jadwal_id).first()

        if not jadwal:
            return None

        else:
            jadwal.id_obat = jadwal_data.id_obat
            jadwal.dosis = jadwal_data.dosis
            jadwal.waktu_minum = jadwal_data.waktu_minum
            jadwal.updated_at = now()

        db.commit()
        db.refresh(jadwal)
        return jadwal
    
    @staticmethod
    def update_patch(db: Session, jadwal_id:int, payload: dict):
        jadwal = db.query(Jadwal).filter(Jadwal.id == jadwal_id).first()

        if not jadwal:
            return None
        
        for key, value in payload.items():

            if not hasattr(Jadwal, key):
                continue

            setattr(jadwal, key, value)

        jadwal.updated_at = now()

        db.commit()
        db.refresh(jadwal)
        return jadwal
    
    @staticmethod
    def delete(db: Session, jadwal_id: int):
        jadwal = db.query(Jadwal).filter(Jadwal.id == jadwal_id).first()

        if not jadwal:
            return None

        db.delete(jadwal)
        db.commit()
        return jadwal
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Jadwal).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Jadwal deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        jadwal = db.query(Jadwal)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Jadwal, key):
                column = getattr(Jadwal, key)
                if "secret" in column.info:
                    continue

                jadwal = jadwal.filter(column == value)
        
        return jadwal.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Jadwal).parse()
        
        if expression is None:
            return []        

        return db.query(Jadwal).filter(expression).all()