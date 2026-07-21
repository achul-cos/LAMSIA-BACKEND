# ------------------------------------------------------------------
# dashboard_repository.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# Dashboard berdasarkan format data dashboard yang diatur oleh dashboard_schema.py
# pada kelas DashboardCreate; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data Dashboard yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session, joinedload

from app.models.history_model import History
from app.models.schedules_model import Schedule
from app.core.history_status import HistoryStatus

from app.core.time import now
from app.core.history_status import HistoryStatus

from datetime import datetime, date

from datetime import timedelta
from collections import defaultdict
from calendar import monthrange

class DashboardRepository:
    @staticmethod
    def get_today_statistics(db: Session):
        today = now().date()

        total_today = (
            db.query(Schedule)
            .filter(
                Schedule.is_active == True
            )
            .count()
        )

        taken_today = (
            db.query(History)
            .filter(
                History.date == today,
                History.status.in_([
                    HistoryStatus.TAKEN,
                    HistoryStatus.LATE
                ])
            )
            .count()
        )

        week_start = today - timedelta(days=6)

        missed_this_week = (
            db.query(History)
            .filter(
                History.date >= week_start,
                History.date <= today,
                History.status == HistoryStatus.MISSED
            )
            .count()
        )

        return {
            "taken_today": taken_today,
            "total_today": total_today,
            "missed_this_week": missed_this_week
        }

    @staticmethod
    def get_next_schedule(db: Session):
        current_time = now()
        today = current_time.date()

        next_history = (
            db.query(History)
            .join(Schedule)
            .options(
                joinedload(History.schedule)
                .joinedload(Schedule.medicine)
            )
            .filter(
                History.date == today,
                History.status == HistoryStatus.PENDING,
                Schedule.time >= current_time.time()
            )
            .order_by(Schedule.time.asc())
            .first()
        )

        if not next_history:
            return {
                "remaining_minutes": None,
                "schedule_time": None,
                "medicine_name": None,
                "is_finished": True
            }
        
        schedule_datetime = datetime.combine(
            today,
            next_history.schedule.time,
            tzinfo=current_time.tzinfo
        )

        remaining_minutes = int(
            (schedule_datetime - current_time).total_seconds() / 60
        )

        return {
            "remaining_minutes": max(remaining_minutes, 0),
            "schedule_time": next_history.schedule.time.strftime("%H:%M"),
            "medicine_name": next_history.schedule.medicine.name,
            "is_finished": False
        }

    @staticmethod
    def get_adherence(db: Session):
        today = now().date()
        month_start = today.replace(day=1)

        success = (
            db.query(History)
            .filter(
                History.date >= month_start,
                History.date <= today,
                History.status.in_([
                    HistoryStatus.TAKEN,
                    HistoryStatus.LATE
                ])
            )
            .count()
        )

        missed = (
            db.query(History)
            .filter(
                History.date >= month_start,
                History.date <= today,
                History.status == HistoryStatus.MISSED
            )
            .count()
        )

        total = success + missed

        adherence = 0

        if total > 0:
            adherence = round((success / total) * 100)
        
        return {
            "percentage": adherence
        }

    @staticmethod
    def get_weekly_adherence(
        db: Session,
        year: int | None = None,
        month: int | None = None
    ):
        today = now().date()
        if year is None:
            year = today.year
        if month is None:
            month = today.month
        month_start = date(
            year,
            month,
            1
        )
        last_day = monthrange(
            year,
            month
        )[1]
        month_end = date(
            year,
            month,
            last_day
        )

        iso_weeks = []
        result = []

        current = month_start

        while current <= month_end:
            week = current.isocalendar().week

            if week not in iso_weeks:
                iso_weeks.append(week)

            current += timedelta(days=1)

        histories = (
            db.query(History)
            .filter(
                History.date >= month_start,
                History.date <= month_end
            )
            .all()
        )

        weeks = defaultdict(
            lambda: {
                "success": 0,
                "missed": 0
            }
        )

        for history in histories:
            week = history.date.isocalendar().week

            if history.status in (
                HistoryStatus.TAKEN,
                HistoryStatus.LATE
            ):
                weeks[week]["success"] += 1
            elif history.status == HistoryStatus.MISSED:
                weeks[week]["missed"] += 1

        for index, iso_week in enumerate(iso_weeks, start=1):
            data = weeks[iso_week]
            total = data["success"] + data["missed"]

            percentage = 0

            if total > 0:
                percentage = round(
                    (data["success"] / total) * 100
                )

            result.append({
                "week": index,
                "label": f"Week {index}",
                "iso_week": iso_week,
                "value": percentage,
            })

        return result

    @staticmethod
    def get_latest_alerts(db: Session):
        histories = (
            db.query(History)
            .options(
                joinedload(History.schedule)
                .joinedload(Schedule.medicine)
            )
            .order_by(History.updated_at.desc())
            .limit(3)
            .all()
        )

        alerts = []

        for history in histories:
            if history.status == HistoryStatus.PENDING:
                continue

            medicine_name = history.schedule.medicine.name
            schedule_time = history.schedule.time.strftime("%H:%M")

            if history.status == HistoryStatus.MISSED:
                alerts.append({
                    "icon": "⚠️",
                    "type": "warning",
                    "text": f"{medicine_name} terlewat diminum pada pukul {schedule_time}",
                    "time": history.updated_at
                })

            elif history.status == HistoryStatus.LATE:
                alerts.append({
                    "icon": "⏰",
                    "type": "late",
                    "text": f"{medicine_name} diminum terlambat",
                    "time": history.update_at
                })

            elif history.status == HistoryStatus.TAKEN:
                alerts.append({
                    "icon": "✅",
                    "type": "success",
                    "text": f"{medicine_name} berhasil diminum",
                    "time": history.update_at
                })

        return alerts

    @staticmethod
    def get_dashboard(db: Session):
        statistics = DashboardRepository.get_today_statistics(db)

        statistics["next_medicine"] = DashboardRepository.get_next_schedule(db)
        statistics["adherence"] = DashboardRepository.get_adherence(db)
        # statistics["blood_pressure"] = {
        #     "systolic": 118,
        #     "diastolic": 78,
        #     "status": "normal"
        # }

        return {
            "statistics": statistics,
            "weekly_adherence" : DashboardRepository.get_weekly_adherence(db),
            "latest_alerts": DashboardRepository.get_latest_alerts(db)
        }
