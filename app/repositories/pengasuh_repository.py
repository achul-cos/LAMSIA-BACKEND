# ------------------------------------------------------------------
# pengasuh_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Pengasuh berdasarkan format data pengasuh yang diatur oleh pengasuh_schema.py
# pada kelas PengasuhCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Pengasuh yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.pengasuh_model import Pengasuh
from app.schemas.pengasuh_schema import PengasuhCreate, PengasuhUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class PengasuhRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data pengasuh
    dengan format data pengasuh sesuai pada pengasuh_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, pengasuh_data: PengasuhCreate):
        pengasuh = Pengasuh(
            name = pengasuh_data.name,
            telephone = pengasuh_data.telephone,
            password = pengasuh_data.password
        )
        db.add(pengasuh)
        db.commit()
        db.refresh(pengasuh)
        return pengasuh
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel pengasuh yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Pengasuh).all()

    @staticmethod
    def get_by_id(db: Session, pengasuh_id: int):
        return(db.query(Pengasuh).filter(Pengasuh.id == pengasuh_id).first())
    
    @staticmethod
    def update_put(db: Session, pengasuh_id: int, pengasuh_data: PengasuhUpdate):
        pengasuh = db.query(Pengasuh).filter(Pengasuh.id == pengasuh_id).first()

        if not pengasuh:
            return None

        else:
            pengasuh.name = pengasuh_data.name
            pengasuh.telephone = pengasuh_data.telephone
            pengasuh.email = pengasuh_data.email
            pengasuh.address = pengasuh_data.address
            pengasuh.family_status = pengasuh_data.family_status
            pengasuh.password = pengasuh_data.password
            pengasuh.updated_at = now()

        db.commit()
        db.refresh(pengasuh)
        return pengasuh
    
    @staticmethod
    def update_patch(db: Session, pengasuh_id:int, payload: dict):
        pengasuh = db.query(Pengasuh).filter(Pengasuh.id == pengasuh_id).first()

        if not pengasuh:
            return None
        
        for key, value in payload.items():

            if not hasattr(Pengasuh, key):
                continue

            setattr(pengasuh, key, value)

        pengasuh.updated_at = now()

        db.commit()
        db.refresh(pengasuh)
        return pengasuh
    
    @staticmethod
    def delete(db: Session, pengasuh_id: int):
        pengasuh = db.query(Pengasuh).filter(Pengasuh.id == pengasuh_id).first()

        if not pengasuh:
            return None

        db.delete(pengasuh)
        db.commit()
        return pengasuh
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Pengasuh).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Pengasuh deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        pengasuh = db.query(Pengasuh)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Pengasuh, key):
                column = getattr(Pengasuh, key)
                if "secret" in column.info:
                    continue

                pengasuh = pengasuh.filter(column == value)
        
        return pengasuh.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Pengasuh).parse()
        
        if expression is None:
            return []        

        return db.query(Pengasuh).filter(expression).all()