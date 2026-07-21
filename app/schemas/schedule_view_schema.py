# ------------------------------------------------------------------
# schedule_view_schema.py
# ------------------------------------------------------------------
# Kode schedule_view_schema.py berfungsi untuk mengatur bagaimana model
# Schedule_view_schema dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Schedule_view_schema.
# Serta bagaimana objek Schedule_view_schema ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import date, time, datetime

# ==============
# Daily Schedule
# ==============

class DailyScheduleItem(BaseModel):
    history_id: int | None = None
    schedule_id: int
    medicine_id: int

    medicine_name: str
    dosage: int

    time: time
    status: str
    taken_at: datetime | None = None

    class Config:
        from_attributes = True

class DailyScheduleResponse(BaseModel):
    date: date
    items: list[DailyScheduleItem]

# ===============
# Weekly Schedule
# ===============

class WeeklyScheduleItem(BaseModel):
    date: date
    day: str
    taken: int
    total: int

class WeeklyScheduleResponse(BaseModel):
    week: list[WeeklyScheduleItem]

# =========================================================
# Gabungan DailyScheduleResponse dan WeeklyScheduleResponse
# =========================================================
class ScheduleViewResponse(BaseModel):
    selected_date: date
    week: list[WeeklyScheduleItem]
    daily: list[DailyScheduleItem]
