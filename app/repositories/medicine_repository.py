# ------------------------------------------------------------------
# medicine_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Medicine berdasarkan format data medicine yang diatur oleh medicine_schema.py
# pada kelas MedicineCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Medicine yang ada.
# ------------------------------------------------------------------
from app.core.time import now
from sqlalchemy.orm import Session
from app.models.medicine_model import Medicine
from app.helper.query_parser import QueryParser
from app.models.schedules_model import Schedule
from app.schemas.medicine_schema import MedicineCreate, MedicineUpdate

class MedicineRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data medicine
    dengan format data medicine sesuai pada medicine_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, medicine_data: MedicineCreate):
        try:
            medicine = Medicine(
                name=medicine_data.name,
                dosage=medicine_data.dosage,
                form=medicine_data.form,
                quantity=medicine_data.quantity,
                kompartemen=medicine_data.kompartemen,
                repeat=medicine_data.repeat
            )

            db.add(medicine)
            db.flush()

            for schedule_time in medicine_data.times:
                schedule = Schedule(
                    medicine_id=medicine.id,
                    time=schedule_time
                )

                db.add(schedule)

            db.commit()
            db.refresh(medicine)
            return medicine
        except Exception:
            db.rollback()
            raise
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel medicine yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Medicine).all()

    @staticmethod
    def get_by_id(db: Session, medicine_id: int):
        return(db.query(Medicine).filter(Medicine.id == medicine_id).first())
    
    @staticmethod
    def update_put(db: Session, medicine_id: int, medicine_data: MedicineUpdate):
        medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

        if not medicine:
            return None

        else:
            #medicine.atribute_1 = medicine_data.atribut_1
            #medicine.atribut_2 = medicine_data.atribut_2
            #medicine.atribut_3 = medicine_data.atribut_3
            medicine.updated_at = now()

        db.commit()
        db.refresh(medicine)
        return medicine
    
    @staticmethod
    def update_patch(db: Session, medicine_id:int, payload: dict):
        medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

        if not medicine:
            return None
        
        for key, value in payload.items():

            if not hasattr(Medicine, key):
                continue

            setattr(medicine, key, value)

        medicine.updated_at = now()

        db.commit()
        db.refresh(medicine)
        return medicine
    
    @staticmethod
    def delete(db: Session, medicine_id: int):
        medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

        if not medicine:
            return None

        db.delete(medicine)
        db.commit()
        return medicine
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Medicine).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Medicine deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        medicine = db.query(Medicine)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Medicine, key):
                column = getattr(Medicine, key)
                if "secret" in column.info:
                    continue

                medicine = medicine.filter(column == value)
        
        return medicine.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Medicine).parse()
        
        if expression is None:
            return []        

        return db.query(Medicine).filter(expression).all()