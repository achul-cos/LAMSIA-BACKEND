# ------------------------------------------------------------------
# sonar_schema.py
# ------------------------------------------------------------------
# Kode sonar_schema.py berfungsi untuk mengatur bagaimana model
# Sonar dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek Sonar.
# Serta bagaimana objek Sonar ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SonarCreate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat Sonar yang baru.

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
    
    sonar_id: str
    jarak: str
    lebihJauh: str

class SonarUpdate(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin mengubah suatu Sonar.

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
    
    sonar_id: str
    jarak: str
    lebihJauh: str 

class SonarResponse(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat Sonar.

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
    sonar_id: str
    jarak: str
    lebihJauh: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute = True