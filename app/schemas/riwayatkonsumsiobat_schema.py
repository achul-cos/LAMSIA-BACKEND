# ------------------------------------------------------------------
# riwayatkonsumsiobat_schema.py
# ------------------------------------------------------------------
# Kode riwayatkonsumsiobat_schema.py berfungsi untuk mengatur bagaimana model
# Riwayatkonsumsiobat dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Riwayatkonsumsiobat.
# Serta bagaimana objek Riwayatkonsumsiobat ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class RiwayatkonsumsiobatCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Riwayatkonsumsiobat yang baru.

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
    
    kompartemen: int
    waktu_minum: datetime

class RiwayatkonsumsiobatUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Riwayatkonsumsiobat.

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
    
    kompartemen: int
    waktu_minum: datetime
    waktu_balikin: datetime 

class RiwayatkonsumsiobatResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Riwayatkonsumsiobat.

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
    kompartemen: int
    waktu_minum: datetime
    waktu_balikin: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute = True