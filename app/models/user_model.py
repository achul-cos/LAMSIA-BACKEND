# ------------------------------------------------------------------
# user_model.py
# ------------------------------------------------------------------
# Kode yang digunakan untuk melakukan pemodelan class atau
# objek User pada sistem. Pemodelan mendefinisikan objek User
# memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime
from app.core.time import now

# Objek User memiliki atribut id, username, telephone dan password
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    telephone = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False, info={"secret"})
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now)