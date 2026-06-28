import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.medicine_model import Medicine
from app.models.pengasuh_model import Pengasuh
from app.models.sensorresult_model import Sensorresult
from app.models.user_model import User

def main():
  print("Menghubungkan ke MySQL Laragon")
  try:
    Base.metadata.create_all(bind=engine)
    print("SUKSES: Tabel dan kolom kosong berhasil dibuat di database Laragon")
  except Exception as e:
    print(f"ERROR: Gagal membuat tabel. Pesan error: {e}")

if __name__ == "__main__":
  main()
