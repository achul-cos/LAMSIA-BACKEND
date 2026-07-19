# ------------------------------------------------------------------
# konsumsiobat_model.py
# ------------------------------------------------------------------
# konsumsiobat_model.py digunakan untuk melakukan pemodelan class atau
# objek konsumsiobat pada sistem. Pemodelan mendefinisikan
# objek konsumsiobat memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class Konsumsiobat(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek konsumsiobat
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "konsumsiobats"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    id_obat = Column(Integer, ForeignKey("obats.id"), nullable=False)
    id_kotakobat = Column(Integer, ForeignKey("kotakobats.id"), nullable=False)
    waktu_minum = Column(DateTime(), nullable=False)
    waktu_balikin = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())    

    obats = relationship("Obat", back_populates="konsumsiobats")
    kotakobats = relationship("Kotakobat", back_populates="konsumsiobats")