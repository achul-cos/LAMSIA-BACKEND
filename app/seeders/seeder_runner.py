from cli.utils.resource_name import ResourceName
from app.seeders.base_seeder import BaseSeeder
import importlib
import inspect
import pkgutil
import app.seeders

from app.models.obat_model import Obat
from app.models.jadwal_model import Jadwal
from app.models.riwayatjadwal_model import Riwayatjadwal
from app.models.konsumsiobat_model import Konsumsiobat
from app.models.kotakobat_model import Kotakobat

def get_seeders():
    seeders = []

    # Pkgutil mengambil semua nama-nama file pada path seeder,
    # lalu menginterasikannya.
    for _, module_name, _ in pkgutil.iter_modules(app.seeders.__path__):

        # Jika module_name nya base_seeder, skip aja
        # soalnya itu abstract dari class seeder lainya
        if module_name == "base_seeder" or module_name == "seeder_runner":
            continue

        # import module berdasarkan nama dari module_name
        module = importlib.import_module(f"app.seeders.{module_name}")

        # Kita ingin mengambil object class didalam module tersebut
        # menggunakan inspect.getmembers(module, inspect.isclass) dan menghasilkan
        # nilai berupa class-class didalam module,
        # asumsikan didalam suatu module terdapat banyak class, karena import module juga
        # Maka kita iterasikan setiap nilai class yang kita dapatkan pada suatu module
        for _, obj in inspect.getmembers(module, inspect.isclass):

            # Class Seeder yang sesungguhnya adalah, class yang mewarisi class BaseSeeder
            # dan dia bukanlah BaseSeeder
            if issubclass(obj, BaseSeeder) and obj is not BaseSeeder:
                seeders.append(obj())

    return seeders

def run_seeders():
    seeders = get_seeders()

    if (seeders.count == 0):
        print("Seeder Runner : Can't Run Seed. Karena belum ada seeder yang dibuat.")
        return

    for seeder in seeders:
        try:
            seeder.run()
        except Exception as e:
            print(f"Seeder Error : Can't Run {seeder.__class__.__name__}. Error Message : {e}")

    print("Seeder : All Seeder done executed")

def run_seeder(seeder):
    
    seeder_path = f"app.seeders.{ResourceName(seeder).seeder_file}"

    if importlib.util.find_spec(seeder_path) is None:
        print(f"Seeder Error : {seeder} haven't created yet before")
        return
    
    module = importlib.import_module(f"{seeder_path}")

    seeder_class_name = ResourceName(seeder).seeder_class
    seeder_class = getattr(module, seeder_class_name)

    seeder = seeder_class()
    seeder.run()

    # print(f"Seeder : {seeder} done executed")