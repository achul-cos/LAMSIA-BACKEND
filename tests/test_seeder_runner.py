from app.seeders.seeder_runner import get_seeders
from app.factories.factory_seeder import FactorySeeder

# get_seeders()

Factory = FactorySeeder()

Factory.run()