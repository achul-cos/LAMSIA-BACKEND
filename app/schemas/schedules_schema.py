# ------------------------------------------------------------------
# schedules_schema.py
# ------------------------------------------------------------------
# Kode schedules_schema.py berfungsi untuk mengatur bagaimana model
# Schedules dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Schedules.
# Serta bagaimana objek Schedules ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime, time

class SchedulesBase(BaseModel):
    medicine_id: int
    time: time
    is_active: bool = True

class SchedulesCreate(SchedulesBase):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Schedules yang baru.

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
    

class SchedulesUpdate(SchedulesBase):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Schedules.

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
     

class SchedulesResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Schedules.

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
