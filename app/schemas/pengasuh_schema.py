# ------------------------------------------------------------------
# pengasuh_schema.py
# ------------------------------------------------------------------
# Kode pengasuh_schema.py berfungsi untuk mengatur bagaimana model
# Pengasuh dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Pengasuh.
# Serta bagaimana objek Pengasuh ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class PengasuhCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Pengasuh yang baru.

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
    
    name: str
    telephone: str
    email: str
    address: str
    family_status: Enum
    password: str

class PengasuhResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Pengasuh.

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
    telephone: str
    email: str
    address: str
    family_status: Enum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute = True