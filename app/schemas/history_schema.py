# ------------------------------------------------------------------
# histories_schema.py
# ------------------------------------------------------------------
# Kode histories_schema.py berfungsi untuk mengatur bagaimana model
# Histories dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Histories.
# Serta bagaimana objek Histories ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import date, datetime

class HistoryBase(BaseModel):
    schedule_id: int
    date: date
    status: str
    taken_at: datetime | None = None

class HistoryCreate(HistoryBase):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Histories yang baru.

    Class Schematic:
    <column_1>: <column_type_data_1>
    <column_2>: <column_type_data_2>
    ...

    <column> (variabel)             : nama columnnya
    <column_type_data> (instance)   : tipe data dari columnnya

    Example:
    user_name: str
    email: EmailStr
    student_number: int
    birth: datetime
    password: str
    """

class HistoryUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Histories.

    Class Schematic:
    <column_1>: <column_type_data_1>
    <column_2>: <column_type_data_2>
    ...

    <column> (variabel)             : nama columnnya
    <column_type_data> (instance)   : tipe data dari columnnya

    Example:
    user_name: str
    email: EmailStr
    student_number: int
    birth: datetime
    password: str
    """
    status: str | None = None
    taken_at: datetime | None = None

class HistoryResponse(HistoryBase):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Histories.

    Note:
    Penting untuk tidak menampikan data yang bersifat rahasia,
    seperti password atau data lainya.

    Class Schematic:
    <column_1>: <column_type_data_1>
    <column_2>: <column_type_data_2>
    ...

    <column> (variabel)             : nama columnnya
    <column_type_data> (instance)   : tipe data dari columnnya

    example:
    id: int
    user_name: str
    email: EmailStr
    created_at: datetime            # Timestamp data, opsional ditampilkan
    updated_at: datetime            # Timestamp data, opsional ditampilkan
    """
    
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MedicationHistoryResponse(BaseModel):
    history_id: int
    date: date
    time: str
    medicine_name: str
    dosage: int
    form: str
    status: str
    taken_at: datetime | None = None

    class Config:
        from_attributes = True

class HistoryChartItem(BaseModel):
    day: str
    taken: int
    late: int

class HistorySummaryItem(BaseModel):
    date: date
    taken: int
    missed: int
    late: int
    items: list[MedicationHistoryResponse]

class MedicationChartItem(BaseModel):
    day: str
    taken: int
    late: int

class MedicationChartResponse(BaseModel):
    data: list[MedicationChartItem]
