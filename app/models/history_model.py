
# ------------------------------------------------------------------
# history_model.py
# ------------------------------------------------------------------
# history_model.py digunakan untuk melakukan pemodelan class atau
# objek history pada sistem. Pemodelan mendefinisikan
# objek history memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String
from app.core.database import Base

class History(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek history
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
            