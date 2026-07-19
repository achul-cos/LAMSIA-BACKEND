# ------------------------------------------------------------------
# konsumsiobat_schema.py
# ------------------------------------------------------------------
# Kode konsumsiobat_schema.py berfungsi untuk mengatur bagaimana model
# Konsumsiobat dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Konsumsiobat.
# Serta bagaimana objek Konsumsiobat ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class KonsumsiobatCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Konsumsiobat yang baru.

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
    id_kotakobat: int
    waktu_minum: datetime

class KonsumsiobatUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Konsumsiobat.

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
    id_kotakobat: int
    waktu_minum: datetime
    waktu_balikin: datetime 

class KonsumsiobatResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Konsumsiobat.

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
    id_kotakobat: int
    waktu_minum: datetime
    waktu_balikin: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True