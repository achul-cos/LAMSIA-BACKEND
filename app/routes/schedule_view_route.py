# ------------------------------------------------------------------
# schedule_view_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /schedule_views yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /schedule_views akan didaftarkan pada main.py
# ------------------------------------------------------------------
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.history_repository import HistoryRepository
from app.schemas.schedule_view_schema import (
    DailyScheduleResponse,
    WeeklyScheduleResponse
)

router = APIRouter(
    prefix="/schedule-view",
    tags=["Schedule Views"]
)

@router.get("/daily", response_model=DailyScheduleResponse)
def get_daily_schedule(
    date: date,
    db: Session = Depends(get_db)
):
    return HistoryRepository.get_daily_schedule(
        db,
        date
    )

@router.get("/weekly", response_model=WeeklyScheduleResponse)
def get_weekly_schedule(
    date: date,
    db: Session = Depends(get_db)
):
    return HistoryRepository.get_weekly_summary(
        db,
        date
    )
