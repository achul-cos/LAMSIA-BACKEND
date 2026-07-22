# ------------------------------------------------------------------
# jadwal_schema.py
# ------------------------------------------------------------------
# Kode jadwal_schema.py berfungsi untuk mengatur bagaimana model
# Jadwal dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Jadwal.
# Serta bagaimana objek Jadwal ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime, time
from app.schemas.riwayatjadwal_schema import RiwayatjadwalResponse
from app.schemas.konsumsiobat_schema import KonsumsiobatResponse
from app.schemas.obat_schema import ObatResponse
from enum import Enum

class JadwalCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Jadwal yang baru.

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
    
    id_obat: int
    dosis: int
    waktu_minum: time

class JadwalUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Jadwal.

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
    
    id_obat: int
    dosis: int
    waktu_minum: time 

class RiwayatJadwalResponseAtJadwal(RiwayatjadwalResponse):
    is_terlambat: bool | None = None
    is_terlewat: bool | None = None
    waktu_terlambat: float | None = None
    riwayat_konsumsi: KonsumsiobatResponse | None = None

class JadwalResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Jadwal.

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
    id_obat: int
    dosis: int
    waktu_minum: time
    riwayatjadwals: list[RiwayatJadwalResponseAtJadwal] | None = None
    obat: ObatResponse | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
