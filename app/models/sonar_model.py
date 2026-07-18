# ------------------------------------------------------------------
# sonar_model.py
# ------------------------------------------------------------------
# sonar_model.py digunakan untuk melakukan pemodelan class atau
# objek sonar pada sistem. Pemodelan mendefinisikan
# objek sonar memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from app.core.database import Base
from app.core.time import now

class Sonar(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek sonar
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "sonars"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    sonar_id = Column(String(100), nullable=False)
    jarak = Column(String(100), nullable=False)
    lebihJauh = Column(String(100), nullable=False)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())    
            