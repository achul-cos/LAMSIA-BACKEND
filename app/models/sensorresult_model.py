# ------------------------------------------------------------------
# sensorresult_model.py
# ------------------------------------------------------------------
# sensorresult_model.py digunakan untuk melakukan pemodelan class atau
# objek sensorresult pada sistem. Pemodelan mendefinisikan
# objek sensorresult memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from app.core.database import Base
from app.core.time import now

class Sensorresult(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek sensorresult
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "sensorresults"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    heart_rate = Column(Integer, nullable=False)
    blood_saturation = Column(Float, nullable=False)
    created_at = Column(DateTime(), default=now)
    updated_at = Column(DateTime(), default=now)
