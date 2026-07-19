# ------------------------------------------------------------------
# riwayatjadwal_schema.py
# ------------------------------------------------------------------
# Kode riwayatjadwal_schema.py berfungsi untuk mengatur bagaimana model
# Riwayatjadwal dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Riwayatjadwal.
# Serta bagaimana objek Riwayatjadwal ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class RiwayatjadwalCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Riwayatjadwal yang baru.

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
    
    id_jadwal: int
    waktu_riwayat: datetime

class RiwayatjadwalUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Riwayatjadwal.

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
    
    id_jadwal: int
    waktu_riwayat: datetime 

class RiwayatjadwalResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Riwayatjadwal.

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
    id_jadwal: int
    waktu_riwayat: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True