from cli.utils.resource_name import ResourceName

class SchemaTemplate:
    def __init__(self, schema_name: str):
        self.schema_name = schema_name
        self.schema_file_name = ResourceName(self.schema_name).schema_file
        self.schema_class_name = ResourceName(self.schema_name).class_name
        self.schema_model_file = ResourceName(self.schema_name).model_file
        self.schema_model_class_name = ResourceName(self.schema_name).class_name
        self.schema_column_name = ResourceName(self.schema_name).singular

    def build(
        self, 
        schema_create:str = "", 
        schema_response:str = (f"""
    id: int
    created_at: datetime
    updated_at: datetime"""
    )):
        return (
f'''# ------------------------------------------------------------------
# {self.schema_file_name}
# ------------------------------------------------------------------
# Kode {self.schema_file_name} berfungsi untuk mengatur bagaimana model
# {self.schema_class_name} dibuat (CREATE) serta melakukan validasi
# terhadap data yang digunakan untuk membuat objek {self.schema_class_name}.
# Serta bagaimana objek {self.schema_class_name} ditampilkan datanya (SHOW)
# ------------------------------------------------------------------
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class {self.schema_class_name}Create(BaseModel):
    """
    Merancang persyaratan data-data yang diberikan pengguna
    Setiap ingin membuat {self.schema_class_name} yang baru.

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
    {schema_create}

class {self.schema_class_name}Response(BaseModel):
    """
    Merancangan data yang dapat ditampilkan setiap kali pengguna
    ingin melihat {self.schema_class_name}.

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
    {schema_response}

    class Config:
        from_attribute = True''')