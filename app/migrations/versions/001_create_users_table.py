
# ------------------------------------------------------------------
# 001_create_users_table.py
# ------------------------------------------------------------------
# 001_create_users_table.py yaitu kode yang mendefinisikan tabel migration dari
# model user_model.py. Kode ditulis dengan format ORM
# pewarisan dari class Base, yang terdiri dari nama column, tipe data,
# dan atribut lainya dari column tersebut
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Table
from app.core.database import Base

def upgrade(engine):
    """
    fungsi upgrade(), yaitu fungsi yang diprogram untuk mendefinisikan column,
    tipe data, atribut dan lainya terkait column tersebut. Kode ditulis
    mengikuti rancangan dari model user_model.py seharusnya.
    """
    users = Table("users", Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String(100), nullable=False),
        Column("telephone", String(100), nullable=False),
        Column("password", String(255), nullable=False)
    )

    users.create(
        bind=engine,
        checkfirst=True
    )
    

def downgrade(engine):
    """
    fungsi down(), yaitu fungsi yang diprogram untuk menghapus column,
    tipe data, atribut dan lainya terkait column tersebut secara
    spesifik atau kesuluruhan tabel.
    """
    pass
        