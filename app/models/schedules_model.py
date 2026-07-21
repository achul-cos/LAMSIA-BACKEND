# ------------------------------------------------------------------
# schedules_model.py
# ------------------------------------------------------------------
# schedules_model.py digunakan untuk melakukan pemodelan class atau
# objek schedules pada sistem. Pemodelan mendefinisikan
# objek schedules memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, Boolean, Time, DateTime, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.time import now

class Schedule(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek schedules
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "schedules"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    time = Column(Time, nullable=False)
    period = Column(VARCHAR(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(), default=now)
    updated_at = Column(DateTime(), default=now, onupdate=now)

    medicine = relationship(
        "Medicine",
        back_populates="schedules"
    )

    histories = relationship(
        "History",
        back_populates="schedule",
        cascade="all, delete-orphan"
    )
