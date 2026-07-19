# ------------------------------------------------------------------
# obat_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Obat berdasarkan format data obat yang diatur oleh obat_schema.py
# pada kelas ObatCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Obat yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.obat_model import Obat
from app.schemas.obat_schema import ObatCreate, ObatUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class ObatRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data obat
    dengan format data obat sesuai pada obat_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, obat_data: ObatCreate):
        obat = Obat(
            nama_obat = obat_data.nama_obat,
            takaran_obat = obat_data.takaran_obat
        )
        db.add(obat)
        db.commit()
        db.refresh(obat)
        return obat
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel obat yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Obat).all()

    @staticmethod
    def get_by_id(db: Session, obat_id: int):
        return(db.query(Obat).filter(Obat.id == obat_id).first())
    
    @staticmethod
    def update_put(db: Session, obat_id: int, obat_data: ObatUpdate):
        obat = db.query(Obat).filter(Obat.id == obat_id).first()

        if not obat:
            return None

        else:
            obat.nama_obat = obat_data.nama_obat
            obat.takaran_obat = obat_data.takaran_obat
            obat.updated_at = now()

        db.commit()
        db.refresh(obat)
        return obat
    
    @staticmethod
    def update_patch(db: Session, obat_id:int, payload: dict):
        obat = db.query(Obat).filter(Obat.id == obat_id).first()

        if not obat:
            return None
        
        for key, value in payload.items():

            if not hasattr(Obat, key):
                continue

            setattr(obat, key, value)

        obat.updated_at = now()

        db.commit()
        db.refresh(obat)
        return obat
    
    @staticmethod
    def delete(db: Session, obat_id: int):
        obat = db.query(Obat).filter(Obat.id == obat_id).first()

        if not obat:
            return None

        db.delete(obat)
        db.commit()
        return obat
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Obat).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Obat deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        obat = db.query(Obat)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Obat, key):
                column = getattr(Obat, key)
                if "secret" in column.info:
                    continue

                obat = obat.filter(column == value)
        
        return obat.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Obat).parse()
        
        if expression is None:
            return []        

        return db.query(Obat).filter(expression).all()