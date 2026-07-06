# ------------------------------------------------------------------
# medicine_schema.py
# ------------------------------------------------------------------
# Kode medicine_schema.py berfungsi untuk mengatur bagaimana model
# Medicine dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Medicine.
# Serta bagaimana objek Medicine ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel, field_validator
from datetime import datetime, time
from app.schemas.schedules_schema import SchedulesResponse

class MedicineBase(BaseModel):
    name: str
    dosage: int
    form: str
    times: list[time]
    quantity: int
    kompartemen: int
    repeat: str

    @field_validator("times")
    @classmethod
    def validate_times(cls, value):
        if len(value) == 0:
            raise ValueError("Minimal harus ada satu jadwal minum.")
        return value

class MedicineCreate(MedicineBase):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Medicine yang baru.

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

class MedicineUpdate(MedicineBase):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Medicine.

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

class MedicineResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Medicine.

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
    name: str
    dosage: int
    form: str
    quantity: int
    kompartemen: int
    repeat: str
    created_at: datetime
    updated_at: datetime

    schedules: list[SchedulesResponse]

    class Config:
        from_attributes = True
