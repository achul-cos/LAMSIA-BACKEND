# ------------------------------------------------------------------
# medicine_schema.py
# ------------------------------------------------------------------
# Kode medicine_schema.py melakukan otorisasi kepada kode lainya pada sistem
# yang ingin menggunakan objek user. Otorisasi yang dilakukan
# seperti format data yang seharusnya diinput oleh pengguna saat akan
# menambahkan user baru, dan bagaimana sistem memberikan respon berupa
# data atribut objek User.
# ------------------------------------------------------------------
from pydantic import BaseModel

# MedicineCreate mendefinisikan bahwa untuk melakukan interaksi create objek Medicine, membutuhkan data-data sesuai dengan medicine_model.py
class MedicineCreate(BaseModel):
    """
    Isi pada bagian ini, sesuai rancangan atribut pada data 
    medicine_model.py dan sesuaikan juga dengan tipe datanya,
    tetapi tidak perlu menambahkan id nya, contoh:

    ------------------------------------------------------------------
    medicine_model.py
    ------------------------------------------------------------------

    class Medicine(Base):
        __tablename__ = "medicines"
        id = Column(Integer, primary_key=True, index=True)
        medicineName = Column(String(100), nullable=False)
        medicinePassword = Column(String(100), nullable=False)
    ------------------------------------------------------------------

    Maka pada kode medicine_schema.py, seharusnya dituliskan sebagai berikut:

    class MedicineCreate(BaseModel):
        medicineName: str
        medicinePassword: str
    """

# MedicineResponse mendefinisikan bahwa untuk melakukan interaksi get atau SHOW pada objek Medicine, dapat menampilkan data-data sebagai berikut:
class MedicineUserResponse(BaseModel):

    """
    Berdasrkan dengan intruksi diatas, pada bagian ini dituliskan serupa
    dengan class MedicineCreate. Tetapi pada bagian
    password itu disembunyikan demi keamanan, serta ditambahkan data
    id dengan tipe data int untuk dapat memberikan data int. Sebagai contoh.

    class MedicineUserResponse(BaseModel):
        id: int
        medicineName: str
    """

    class Config:
        from_attribute = True
        