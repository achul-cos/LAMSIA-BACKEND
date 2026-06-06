# ------------------------------------------------------------------
# user_schema.py
# ------------------------------------------------------------------
# Kode user_schema.py melakukan otorisasi kepada kode lainya pada sistem
# yang ingin menggunakan objek user. Otorisasi yang dilakukan
# seperti format data yang seharusnya diinput oleh pengguna saat akan
# menambahkan user baru, dan bagaimana sistem memberikan respon berupa
# data atribut objek User.
# ------------------------------------------------------------------
from pydantic import BaseModel

# UserCreate mendefinisikan bahwa untuk melakukan interaksi create objek User, membutuhkan data-data sesuai dengan user_model.py
class UserCreate(BaseModel):
    """
    Isi pada bagian ini, sesuai rancangan atribut pada data 
    user_model.py dan sesuaikan juga dengan tipe datanya,
    tetapi tidak perlu menambahkan id nya, contoh:

    ------------------------------------------------------------------
    user_model.py
    ------------------------------------------------------------------

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        userName = Column(String(100), nullable=False)
        userPassword = Column(String(100), nullable=False)
    ------------------------------------------------------------------

    Maka pada kode user_schema.py, seharusnya dituliskan sebagai berikut:

    class UserCreate(BaseModel):
        userName: str
        userPassword: str
    """
    
    username: str
    telephone: str
    password: str

# UserResponse mendefinisikan bahwa untuk melakukan interaksi get atau SHOW pada objek User, dapat menampilkan data-data sebagai berikut:
class UserResponse(BaseModel):

    """
    Berdasrkan dengan intruksi diatas, pada bagian ini dituliskan serupa
    dengan class UserCreate. Tetapi pada bagian
    password itu disembunyikan demi keamanan, serta ditambahkan data
    id dengan tipe data int untuk dapat memberikan data int. Sebagai contoh.

    class UserUserResponse(BaseModel):
        id: int
        userName: str
    """
    
    id: int
    username: str
    telephone: str

    class Config:
        from_attribute = True