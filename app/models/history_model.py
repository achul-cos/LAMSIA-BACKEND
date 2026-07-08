# ------------------------------------------------------------------
# history_model.py
# ------------------------------------------------------------------
# histories_model.py digunakan untuk melakukan pemodelan class atau
# objek histories pada sistem. Pemodelan mendefinisikan
# objek histories memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, VARCHAR, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class History(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek histories
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "histories"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(VARCHAR(20), nullable=False)
    taken_at = Column(DateTime())
    created_at = Column(DateTime(), default=now)
    updated_at = Column(DateTime(), default=now, onupdate=now)

    schedule = relationship(
        "Schedule",
        back_populates="histories"
    )
