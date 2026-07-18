import numpy as np
from sqlalchemy import text

from app.core.database import SessionLocal

def get_ir_data(limit=2000):

    session = SessionLocal()

    try:
        result = session.execute(
            text("""
                SELECT ir
                FROM sensormaxes
                ORDER BY id DESC
                LIMIT :limit
            """),
            {"limit": limit}
        )

        rows = result.fetchall()

    finally:
        session.close()

    # Urutkan kembali agar menjadi data lama -> baru
    rows = rows[::-1]

    ir = np.array([row[0] for row in rows])

    return ir
