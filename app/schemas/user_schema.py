# ------------------------------------------------------------------
# user_schema.py
# ------------------------------------------------------------------
# Kode ini melakukan otorisasi kepada kode lainya pada sistem
# yang ingin menggunakan objek user. Otorisasi yang dilakukan
# seperti format data yang seharusnya diinput oleh pengguna saat akan
# menambahkan user baru, dan bagaimana sistem memberikan respon berupa
# data atribut objek User.
# ------------------------------------------------------------------
from pydantic import BaseModel

# UserCreate mendefinisikan bahwa untuk membuat user, membutuhkan data username, telephone dan password. Dan setiap data tersebut bertipe string
class UserCreate(BaseModel):
    username: str
    telephone: str
    password: str

# UserResponse mendefinisikan bahwa setiap data yang diakses dari objek user, hanya memberikan data id, username dan telephone. Guna mencegah tidak memberikan data penting seperti password.
class UserResponse(BaseModel):
    id: int
    username: str
    telephone: str

    class Config:
        from_attribute = True