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
from sqlalchemy import and_
from datetime import date, timedelta

from app.models.history_model import History
from app.models.schedules_model import Schedule
from app.models.medicine_model import Medicine

from app.schemas.history_schema import HistoryCreate, HistoryUpdate
from app.schemas.schedule_view_schema import (
    DailyScheduleItem,
    DailyScheduleResponse,
    ScheduleViewResponse
)

from app.core.history_status import HistoryStatus

from sqlalchemy.orm import joinedload
from app.helper.query_parser import QueryParser

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
    def get_medication_history(db: Session):
        histories = (
            db.query(History)
            .join(History.schedule)
            .join(Schedule.medicine)
            .all()
        )

        results = []

        for history in histories:
            results.append({
                "history_id": history.id,
                "date": history.date,
                "time": history.schedule.time.strftime("%H:%M"),
                "medicine_name": history.schedule.medicine.name,
                "dosage": history.schedule.medicine.dosage,
                "form": history.schedule.medicine.form,
                "status": history.status,
                "taken_at": history.taken_at
            })

        return results
    
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

    @staticmethod
    def get_daily_schedule(
        db: Session,
        selected_date: date
    ):
        schedules = (
            db.query(Schedule, History)
            .join(Schedule.medicine)
            .outerjoin(
                History,
                and_(
                    History.schedule_id == Schedule.id,
                    History.date == selected_date
                )
            )
            .filter(Schedule.is_active == True)
            .order_by(Schedule.time)
            .all()
        )

        items = []

        for schedule, history in schedules:
            medicine = schedule.medicine

            items.append(
                DailyScheduleItem(
                    history_id=history.id if history else None,
                    schedule_id=schedule.id,
                    medicine_id=medicine.id,
                    medicine_name=medicine.name,
                    dosage=medicine.dosage,
                    time=schedule.time,
                    status=history.status if history else "pending",
                    taken_at=history.taken_at if history else None,
                )
            )

        return DailyScheduleResponse(
            date=selected_date,
            items=items
        )

    @staticmethod
    def get_weekly_summary(
        db: Session,
        selected_date: date
    ):
        start_of_week = selected_date - timedelta(days=selected_date.weekday())

        week = []

        for i in range(7):
            current_date = start_of_week + timedelta(days=i)

            histories = (
                db.query(History)
                .filter(History.date == current_date)
                .all()
            )

            total = len(histories)

            taken = sum(
                1
                for history in histories 
                if history.status == HistoryStatus.TAKEN
            )

            week.append(
                WeeklyScheduleItem(
                    date=current_date,
                    day=current_date.strftime("%a"),
                    taken=taken,
                    total=total
                )
            )

        return WeeklyScheduleResponse(
            week=week
        )

    @staticmethod
    def get_schedule_view(
        db: Session,
        selected_date: date
    ):
        week = HistoryRepository.get_weekly_summary(
            db,
            selected_date
        )

        daily = HistoryRepository.get_daily_schedule(
            db,
            selected_date
        )

        return ScheduleViewResponse(
            selected_date=selected_date,
            week=week,
            daily=daily
        )
