# ------------------------------------------------------------------
# database.py
# ------------------------------------------------------------------
# Kode yang digunakan oleh sistem untuk melakukan interaksi dengan
# database. Dengan cara, kode ini membuat objek yang mewakili database
# itu sendiri. Setiap proses CRUD seperti migration, seeder, query
# pada fungsi dan class didalam sistem. Sistem hanya perlu melakukan
# import objek database pada kode ini. Jadi tidak perlu melakukan koneksi
# dengan database pada setiap kode yang ingin melakukan CRUD.   
# ------------------------------------------------------------------

from sqlalchemy import create_engine                        # import fungsi create_engine dari package sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base   # import class sessionmaker, fungsi declarative_base dari package sqlalchemy
from dotenv import load_dotenv                              # import fungsi load_dotenv dari package dotenv

import os                                                   # import class os dari python, os digunakan untuk mengakses operasi sistem yang menjalankan python. Seperti menambahkan, menghapus atau mengakses sebuah file atau dokumen.

# Menjalankan fungsi load_dotenv dari dotenv, untuk mencari file .env pada proyek, dan mendaftarkan semua variabel .env didalam environment variable sistem (yang dapat diakses oleh OS)
load_dotenv()

# Mendefinisikan variabel .env yang diberada didalam environment variables menjadi variable yang bisa diakses dan dijalankan oleh kode
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Mendefinisikan variabel DATABASE_URL, sebagai alamat atau url untuk mengakses database mysql berdasarkan variabel .env
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Mendefinisikan objek (mesin) database mysql menjadi sebuah objek yang dapat diakses dan dijalankan oleh kode dan sistem
engine = create_engine(
    DATABASE_URL,
    # echo=True,
)

# Mendefinisikan objek sessionmaker sebagai penghubung atau jalur komunikasi menuju engine (database), yang dapat diakses oleh kode pada sistem
SessionLocal = sessionmaker(
    bind=engine,        # bind mendefinisikan alamat (database) untuk berkomunikasi
    autocommit=False,   # autocommit mendefinisikan bahwa setiap proses CRUD yang diprogram pada kode, tidak boleh dijalankan sebelum baris kode db.commit(); Agar menghindari error
    autoflush=False,    # autoflush mendefinisikan bahwa setiap proses CRUD yang diprogram pada kode, tidak langsung menjalankan query pada SQL dalam memproses data.
)

# Base merupakan class yang akan diwariskan dengan model class lainya, yang selanjutnya class yang mewarisi base akan dianggap sebagai class bertipe model SQL (bukan class biasa)
# Class model SQL atau ORM merupakan representasi tabel database
# dalam bentuk class Python. Model berbeda dengan migration.
# Migration bertugas membuat atau mengubah struktur tabel,
# sedangkan model bertugas merepresentasikan tabel tersebut
# dalam kode Python.
Base = declarative_base()