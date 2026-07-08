# ------------------------------------------------------------------
# schedules_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Schedules berdasarkan format data schedules yang diatur oleh schedules_schema.py
# pada kelas SchedulesCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Schedules yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.schedules_model import Schedule
from app.models.medicine_model import Medicine
from app.schemas.schedules_schema import SchedulesCreate, SchedulesUpdate
from app.helper.query_parser import QueryParser
from app.core.time import now

class SchedulesRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data schedules
    dengan format data schedules sesuai pada schedules_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, schedules_data: SchedulesCreate):
        medicine = db.query(Medicine).filter(Medicine.id == schedules_data.medicine_id).first()

        if not medicine:
            raise HTTPException(status_code=404, detail="Medicine tidak ditemukan")

        schedules = Schedule(**schedules_data.model_dump())

        db.add(schedules)
        db.commit()
        db.refresh(schedules)
        return schedules
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel schedules yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(Schedule).options(joinedload(Schedule.medicine)).all()

    @staticmethod
    def get_by_id(db: Session, schedules_id: int):
        schedule = (
            db.query(Schedule)
            .options(joinedload(Schedule.medicine))
            .filter(Schedule.id == schedules_id)
            .first()
        )

        if not schedule:
            raise HTTPException(
                status_code=404,
                detail="Schedule tidak ditemukan."
            )

        return schedule

    @staticmethod
    def get_active(db: Session):
        return (
            db.query(Schedule)
            .options(joinedload(Schedule.medicine))
            .filter(Schedule.is_active == True)
            .all()
        )

    @staticmethod
    def update_put(db: Session, schedules_id: int, schedules_data: SchedulesUpdate):
        schedules = db.query(Schedule).filter(Schedule.id == schedules_id).first()

        if not schedules:
            raise HTTPException(
                status_code=404,
                detail="Schedules tidak ditemukan"
            )

        for key, value in schedules_data.model_dump().items():
            setattr(schedules, key, value)
        # else:
        #     schedules.updated_at = now()

        db.commit()
        db.refresh(schedules)
        return schedules
    
    @staticmethod
    def update_patch(db: Session, schedules_id:int, payload: dict):
        schedules = db.query(Schedule).filter(Schedule.id == schedules_id).first()

        if not schedules:
            return None
        
        for key, value in payload.items():

            if not hasattr(Schedule, key):
                continue

            setattr(schedules, key, value)

        schedules.updated_at = now()

        db.commit()
        db.refresh(schedules)
        return schedules
    
    @staticmethod
    def delete(db: Session, schedules_id: int):
        schedules = db.query(Schedule).filter(Schedule.id == schedules_id).first()

        if not schedules:
            raise HTTPException(
                status_code=404,
                detail="Schedules tidak ditemukan"
            )

        db.delete(schedules)
        db.commit()
        return schedules
    
    @staticmethod
    def delete_all(db: Session):
        db.query(Schedule).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All Schedules deleted successfully"
        }
    
    @staticmethod
    def filter(db: Session, **params):
        schedules = db.query(Schedule)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(Schedule, key):
                column = getattr(Schedule, key)
                if "secret" in column.info:
                    continue

                schedules = schedules.filter(column == value)
        
        return schedules.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, Schedule).parse()
        
        if expression is None:
            return []

        return db.query(Schedule).filter(expression).all()


