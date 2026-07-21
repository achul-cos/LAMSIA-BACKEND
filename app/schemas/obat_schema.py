# ------------------------------------------------------------------
# obat_schema.py
# ------------------------------------------------------------------
# Kode obat_schema.py berfungsi untuk mengatur bagaimana model
# Obat dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Obat.
# Serta bagaimana objek Obat ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel, field_validator
from datetime import datetime, time
from typing import List

class ObatCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Obat yang baru.

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
    
    nama_obat: str
    takaran_obat: str
    dosis: int
    kompartemen: int
    pengulangan: str
    waktu: List[time]

    @field_validator("waktu")
    @classmethod
    def validate_times(cls, value):
        if len(value) == 0:
            raise ValueError("Minimal harus ada satu jadwal minum.")
        return value

class ObatUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Obat.

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

    nama_obat: str
    takaran_obat: str
    dosis: int
    kompartemen: int
    pengulangan: str

class ObatResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Obat.

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
    nama_obat: str
    takaran_obat: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JadwalItem(BaseModel):
    dosis: int
    pengulangan: str
    waktu_minum: time

    class Config:
        from_attributes = True

class ObatListResponse(BaseModel):
    id: int
    nama_obat: str
    takaran_obat: str
    kompartemen: int
    jadwal: List[JadwalItem]

    class Config:
        from_attributes = True
