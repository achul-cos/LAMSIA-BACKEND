# ------------------------------------------------------------------
# medicine_model.py
# ------------------------------------------------------------------
# medicine_model.py digunakan untuk melakukan pemodelan class atau
# objek medicine pada sistem. Pemodelan mendefinisikan
# objek medicine memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, VARCHAR
from app.core.database import Base

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
    times = Column(Integer, nullable=False)
    repeat = Column(VARCHAR(255), nullable=False)
