# ------------------------------------------------------------------
# user_model.py
# ------------------------------------------------------------------
# Kode yang digunakan untuk melakukan pemodelan class atau
# objek User pada sistem. Pemodelan mendefinisikan objek User
# memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String
from app.core.database import Base

# Objek User memiliki atribut id, username, telephone dan password
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    telephone = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False, info={"secret"})