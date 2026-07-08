from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime, timedelta

from app.core.time import now
from app.core.database import SessionLocal
from app.core.history_status import HistoryStatus

from app.repositories.schedules_repository import SchedulesRepository
from app.repositories.history_repository import HistoryRepository

from app.schemas.history_schema import HistoryCreate

scheduler = BackgroundScheduler()

def create_daily_history():
  """
  Membuat history ketika waktu schedule telah tercapai
  """
  db = SessionLocal()

  try:
    schedules = SchedulesRepository.get_all(db)

    current_time = now().time()
    today = now().date()

    for schedule in schedules:
      if current_time < schedule.time:
        continue
      
      history = HistoryRepository.get_by_schedule_and_date(
        db=db,
        schedule_id=schedule.id,
        date=today
      )

      if history:
        continue

      history_data = HistoryCreate(
        schedule_id=schedule.id,
        date=today,
        status=HistoryStatus.PENDING,
        taken_at=None
      )

      HistoryRepository.create(
        db,
        history_data=history_data
      )

      print(
        f"[History Scheduler] History dibuat"
        f"untuk Schedule {schedule.id}"
      )
  except Exception as e:
    print(f"[History Scheduler] Error occurred: {e}")
  finally:
    db.close()

def update_missed_histories():
  db = SessionLocal()

  try:
    histories = HistoryRepository.get_pending_histories(db)
    current_time = now()
    for history in histories:
      schedule_datetime = datetime.combine(
      history.date,
      history.schedule.time,
      tzinfo=current_time.tzinfo
    )

      deadline = schedule_datetime + timedelta(hours=1)

      if current_time >= deadline:
        HistoryRepository.update_status(
          db=db,
          history=history,
          status=HistoryStatus.MISSED
        )
        print(
          f"[History Scheduler]"
          f"History {history.id} berubah menjadi MISSED"
        )
  except Exception as e:
    db.rollback()
    print(e)
  finally:
    db.close()

def start_scheduler():
  scheduler.add_job(
    create_daily_history,
    trigger="interval",
    seconds=10,
    id="history_scheduler",
    replace_existing=True
  )

  scheduler.add_job(
    update_missed_histories,
    trigger="interval",
    seconds=10,
    id="update_missed",
    replace_existing=True
  )

  scheduler.start()

  print("History Scheduler Started")
