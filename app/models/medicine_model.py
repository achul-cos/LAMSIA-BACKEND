# ------------------------------------------------------------------
# medicine_model.py
# ------------------------------------------------------------------
# medicine_model.py digunakan untuk melakukan pemodelan class atau
# objek medicine pada sistem. Pemodelan mendefinisikan
# objek medicine memiliki atribut apa saja. 
# ------------------------------------------------------------------

from app.core.time import now
from app.core.database import Base
from sqlalchemy import Column, Integer, VARCHAR, DateTime
from sqlalchemy.orm import relationship

class Medicine(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek medicine
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "medicines"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), nullable=False)
    dosage = Column(Integer, nullable=False)
    form = Column(VARCHAR(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    kompartemen = Column(Integer, nullable=False)
    repeat = Column(VARCHAR(255), nullable=False)
    created_at = Column(DateTime(), default=now)
    updated_at = Column(DateTime(), default=now)

    schedules = relationship(
        "Schedule",
        back_populates="medicine",
        cascade="all, delete-orphan"
    )
