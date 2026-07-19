# ------------------------------------------------------------------
# konsumsiobat_seeder.py
# ------------------------------------------------------------------
# Kode ini menjalankan fungsi seeder. Seeder adalah data yang ditulis
# secara manual didalam kode ini, lalu dimasukkan kedalam tabel model
# yang ditentukan. Seeder umumnya menjadi initialize data saat database
# baru dibuat atau di migrate.
# ------------------------------------------------------------------

from app.seeders.base_seeder import BaseSeeder
from app.models.konsumsiobat_model import Konsumsiobat
from app.core.database import SessionLocal
from app.repositories.kotakobat_repository import KotakobatRepository
from datetime import datetime, timedelta
import random

class KonsumsiobatSeeder(BaseSeeder):

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

        konsumsiobats = []

        # Mengambil data obat
        kotakobats = KotakobatRepository().get_all(db=db)

        for kotak in kotakobats:

            # data obat
            obat = kotak.obats

            # data jadwal pada obat
            jadwalobats = obat.jadwals

            # Melakukan iterasi pada setiap jadwal yang dimiliki obat
            for jadwal in jadwalobats:

                # Data riwayat jadwal
                riwayatjadwals = jadwal.riwayatjadwals

                # Melakukan iterasi pada setial riwayat jadwal yang dimiliki oleh jadwal
                for riwayat in riwayatjadwals:

                    # waktu riwayat
                    waktu_riwayat = riwayat.waktu_riwayat

                    # waktu konsumsi obat
                    waktu_konsumsi_obat = waktu_riwayat + timedelta(minutes=random.randint(5, 60))

                    # waktu baliki obat
                    waktu_balikin_obat = waktu_konsumsi_obat + timedelta(minutes=random.randint(3, 10))

                    konsumsiobats.append(
                        Konsumsiobat(
                            id_obat = obat.id,
                            id_kotakobat = kotak.id,
                            waktu_minum = waktu_konsumsi_obat,
                            waktu_balikin = waktu_balikin_obat
                        )
                    )

        db.add_all(konsumsiobats)
        db.commit()

        print("Seeder : KonsumsiobatSeeder excuted")