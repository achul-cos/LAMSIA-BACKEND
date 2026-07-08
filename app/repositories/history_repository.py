# ------------------------------------------------------------------
# history_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# History berdasarkan format data history yang diatur oleh history_schema.py
# pada kelas HistoryCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data History yang ada.
# ------------------------------------------------------------------
from app.core.time import now
from sqlalchemy.orm import Session
from datetime import date

from app.models.history_model import History
from app.schemas.history_schema import HistoryCreate, HistoryUpdate
from app.helper.query_parser import QueryParser

from app.core.history_status import HistoryStatus

from sqlalchemy.orm import joinedload

class HistoryRepository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data history
    dengan format data history sesuai pada history_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, history_data: HistoryCreate):
        try:
            history = History(
                schedule_id=history_data.schedule_id,
                date=history_data.date,
                status=history_data.status,
                taken_at=history_data.taken_at
            )
            db.add(history)
            db.commit()
            db.refresh(history)

            return history
        except Exception:
            db.rollback()
            raise

    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel history yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query(History).all()

    @staticmethod
    def get_by_id(db: Session, history_id: int):
        return(db.query(History).filter(History.id == history_id).first())
    
    @staticmethod
    def update_put(db: Session, history_id: int, history_data: HistoryUpdate):
        history = db.query(History).filter(History.id == history_id).first()

        if not history:
            return None

        history.status = history_data.status
        history.taken_at = history_data.taken_at
        history.updated_at = now()

        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def update_patch(db: Session, history_id:int, payload: dict):
        history = db.query(History).filter(History.id == history_id).first()

        if not history:
            return None
        
        for key, value in payload.items():

            if not hasattr(History, key):
                continue

            setattr(history, key, value)

        history.updated_at = now()

        db.commit()
        db.refresh(history)

        return history
    
    def update_status(
        db: Session,
        history: History,
        status: HistoryStatus
    ):
        history.status = status
        history.updated_at = now()

        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def delete(db: Session, history_id: int):
        history = db.query(History).filter(History.id == history_id).first()

        if not history:
            return None

        db.delete(history)
        db.commit()

        return history

    @staticmethod
    def delete_all(db: Session):
        db.query(History).delete(synchronize_session=False)

        db.commit()
        
        return {
            "message": f"All History deleted successfully"
        }

    @staticmethod
    def filter(db: Session, **params):
        history = db.query(History)

        for key, value in params.items():
            if value is None:
                continue

            if hasattr(History, key):
                column = getattr(History, key)

                if "secret" in column.info:
                    continue

                history = history.filter(column == value)

        return history.all()

    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, History).parse()

        if expression is None:
            return []

        return db.query(History).filter(expression).all()

    @staticmethod
    def get_by_schedule_and_date(
        db: Session,
        schedule_id: int,
        date: date
    ):
        return (
            db.query(History)
            .filter(
                History.schedule_id == schedule_id,
                History.date == date
            )
            .first()
        )

    @staticmethod
    def get_pending_histories(db: Session):
        return (
            db.query(History)
            .options(joinedload(History.schedule))
            .filter(History.status == HistoryStatus.PENDING)
            .all()
        )
    
    @staticmethod
    def mark_as_missed(
        db: Session,
        history: History
    ):
        history.status = HistoryStatus.MISSED
        history.updated_at = now()
        db.commit()
        db.refresh(history)

        return history
