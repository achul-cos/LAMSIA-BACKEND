# ------------------------------------------------------------------
# sensormax_model.py
# ------------------------------------------------------------------
# sensormax_model.py digunakan untuk melakukan pemodelan class atau
# objek sensormax pada sistem. Pemodelan mendefinisikan
# objek sensormax memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from app.core.database import Base
from app.core.time import now

class Sensormax(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek sensormax
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "sensormaxes"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    hr = Column(Integer, nullable=False)
    sp = Column(Integer, nullable=False)
    ir = Column(Integer, nullable=False)
    red = Column(Integer, nullable=False)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())    
            