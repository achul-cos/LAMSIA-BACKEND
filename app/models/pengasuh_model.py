# ------------------------------------------------------------------
# pengasuh_model.py
# ------------------------------------------------------------------
# pengasuh_model.py digunakan untuk melakukan pemodelan class atau
# objek pengasuh pada sistem. Pemodelan mendefinisikan
# objek pengasuh memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.core.database import Base
from app.core.time import now

class Pengasuh(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek pengasuh
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "pengasuhs"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    telephone = Column(String(255), nullable=False, unique=True)
    email = Column(String(225), nullable=True)
    address = Column(String(255), default="Indonesia, Kota Batam")
    family_status = Column(Enum('Anak', 'Kerabat', 'Cucu', 'Lansia', 'Anggota Keluarga Lainya'), default='Anggota Keluarga Lainya', nullable=True)
    password = Column(String(255), nullable=False, info={"secret"})
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())
