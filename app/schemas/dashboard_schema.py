# ------------------------------------------------------------------
# dashboard_schema.py
# ------------------------------------------------------------------
# Kode dashboard_schema.py berfungsi untuk mengatur bagaimana model
# Dashboard dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Dashboard.
# Serta bagaimana objek Dashboard ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime

class NextMedicineResponse(BaseModel):
    remaining_minutes: int | None
    schedule_time: str | None
    medicine_name: str | None
    is_finished: bool

class AdherenceResponse(BaseModel):
    percentage: int

# class BloodPressureResponse(BaseModel):
#     systolic: int
#     diastolic: int
#     status: str

class StatisticResponse(BaseModel):
    taken_today: int
    total_today: int
    missed_this_week: int
    next_medicine: NextMedicineResponse | None
    adherence: AdherenceResponse
    # blood_pressure: BloodPressureResponse

class WeeklyAdherenceResponse(BaseModel):
    week: int
    label: str
    iso_week: int
    value: int

class AlertResponse(BaseModel):
    icon: str
    type: str
    text: str
    time: object

class DashboardResponse(BaseModel):
    statistics: StatisticResponse
    weekly_adherence: list[WeeklyAdherenceResponse]
    latest_alerts: list[AlertResponse]
