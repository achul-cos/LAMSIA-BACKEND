# ------------------------------------------------------------------
# riwayatjadwal_model.py
# ------------------------------------------------------------------
# riwayatjadwal_model.py digunakan untuk melakukan pemodelan class atau
# objek riwayatjadwal pada sistem. Pemodelan mendefinisikan
# objek riwayatjadwal memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class Riwayatjadwal(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek riwayatjadwal
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "riwayatjadwals"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    id_jadwal = Column(Integer, ForeignKey("jadwals.id"), nullable=False)
    waktu_riwayat = Column("waktu_riwayat", DateTime(), nullable=False)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())

    jadwals = relationship("Jadwal", back_populates="riwayatjadwals")