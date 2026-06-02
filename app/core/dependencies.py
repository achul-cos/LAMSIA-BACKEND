# ------------------------------------------------------------------
# dependencies.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan sebuah fungsi get_db(), yang digunakan oleh
# system untuk dapat memanggil SessionLocal sebagai jalur komunikasi
# ke engine (atau database). Serta menggunakan session local sebagai
# sebagai class atau objek db itu sendiri yang akan menjalankan perintah
# CRUD.
# ------------------------------------------------------------------
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()