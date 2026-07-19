# ------------------------------------------------------------------
# jadwal_seeder.py
# ------------------------------------------------------------------
# Kode ini menjalankan fungsi seeder. Seeder adalah data yang ditulis
# secara manual didalam kode ini, lalu dimasukkan kedalam tabel model
# yang ditentukan. Seeder umumnya menjadi initialize data saat database
# baru dibuat atau di migrate.
# ------------------------------------------------------------------

from app.seeders.base_seeder import BaseSeeder
from app.core.database import SessionLocal
from app.models.jadwal_model import Jadwal

class JadwalSeeder(BaseSeeder):

    """
    Memasukkan data-data yang dibuat pada kode berikut kedalam
    table database, sebagai data initiliaze sistem.

    Function Schematic:
    from app.models.<model_file> import <model_class>

    <model_table_name> = [
        <model_class>(
            <column_1> = <value_1>,
            <column_2> = <value_2>,
            ...
        ),
        <model_class>(
            <column_1> = <value_1>,
            <column_2> = <value_2>,
            ...
        ),
        ...
    ]

    db.add_all(<model_table_name>)

    <model_file> (file)         : nama file dari model seeder
    <model_class> (object)      : model seeder
    <model_table_name> (list)   : list data-data yang akan ditambahkan
    <column>                    : nama column yang akan diisi nilainya
    <value>                     : nilai dari column yang akan diisi nilainya

    Example:
    from app.models.users import User

    users = [
        User(
            username="Achul",
            telephone="123123",
            password="achul"
        ),
        User(
            username="Steven",
            telephone="456456",
            password="steven"
        )
    ]

    db.add_all(users)
    """

    def run(self):
        db = SessionLocal()

        jadwals = [
            Jadwal(
                id_obat=1,
                dosis=1,
                waktu_minum= "09:00:00",
            ),
            Jadwal(
                id_obat=1,
                dosis=1,
                waktu_minum= "12:00:00",
            ),
            Jadwal(
                id_obat=1,
                dosis=1,
                waktu_minum= "18:00:00",
            ),
            Jadwal(
                id_obat=2,
                dosis=1,
                waktu_minum= "13:00:00",
            ),
            Jadwal(
                id_obat=2,
                dosis=1,
                waktu_minum= "19:00:00",
            ),            
            Jadwal(
                id_obat=3,
                dosis=1,
                waktu_minum= "10:00:00",
            ),
            Jadwal(
                id_obat=4,
                dosis=1,
                waktu_minum= "14:00:00",
            ),
            Jadwal(
                id_obat=4,
                dosis=1,
                waktu_minum= "21:00:00",
            ),                                            
        ]

        db.add_all(jadwals)
        db.commit()

        print("Seeder : JadwalSeeder excuted")