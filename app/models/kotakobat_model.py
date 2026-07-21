# ------------------------------------------------------------------
# kotakobat_model.py
# ------------------------------------------------------------------
# kotakobat_model.py digunakan untuk melakukan pemodelan class atau
# objek kotakobat pada sistem. Pemodelan mendefinisikan
# objek kotakobat memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class Kotakobat(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek kotakobat
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "kotakobats"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    id_obat = Column(Integer, ForeignKey("obats.id"), nullable=False)
    kompartemen = Column(Integer, nullable=False)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now(), onupdate=now())

    obats = relationship("Obat", back_populates="kotakobats")
    konsumsiobats = relationship("Konsumsiobat", back_populates="kotakobats")