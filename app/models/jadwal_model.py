# ------------------------------------------------------------------
# jadwal_model.py
# ------------------------------------------------------------------
# jadwal_model.py digunakan untuk melakukan pemodelan class atau
# objek jadwal pada sistem. Pemodelan mendefinisikan
# objek jadwal memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class Jadwal(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek jadwal
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "jadwals"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    id_obat = Column("id_obat", Integer, ForeignKey("obats.id"), nullable=False)
    dosis = Column("dosis", Integer, nullable=False)
    pengulangan = Column("pengulangan", String(50), nullable=False)
    waktu_minum = Column("waktu_minum", Time, nullable=False)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())    
    
    obat = relationship("Obat" , back_populates="jadwals")
    riwayatjadwals = relationship("Riwayatjadwal", back_populates="jadwals")