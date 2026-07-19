# ------------------------------------------------------------------
# obat_model.py
# ------------------------------------------------------------------
# obat_model.py digunakan untuk melakukan pemodelan class atau
# objek obat pada sistem. Pemodelan mendefinisikan
# objek obat memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class Obat(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek obat
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "obats"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    nama_obat = Column(String, nullable=False)
    takaran_obat = Column(String, nullable=False)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())    

    jadwals = relationship("Jadwal", back_populates="obat")
    kotakobats = relationship("Kotakobat", back_populates="obats")
    konsumsiobats = relationship("Konsumsiobat", back_populates="obats")