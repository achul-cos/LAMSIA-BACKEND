from app.seeders.user_seeder import UserSeeder
from cli.utils.resource_name import ResourceName
import importlib

def run_seeders():
    seeders = [
        UserSeeder()
    ]

    for seeder in seeders:
        seeder.run()

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