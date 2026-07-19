from app.core.database import SessionLocal
from cli.utils.resource_name import ResourceName
import importlib

import inspect
import pkgutil
from app.factories.base_factory import BaseFactory
import app.factories

class FactorySeeder:
    def __init__(self, factory_name: str = "", count: int = 10):
        self.factory_name = factory_name
        self.count = count

    @staticmethod
    def get_factory():
        factories = []

        for _, module_name, _ in pkgutil.iter_modules(app.factories.__path__):

            if module_name == "base_factory" or module_name == "factory_seeder":
                continue

            module = importlib.import_module(f"app.factories.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                
                if issubclass(obj, BaseFactory) and obj is not BaseFactory and obj is not FactorySeeder:
                    factories.append(obj())

        return factories

    def run(self):

        factories = self.get_factory()

        if (factories.count == 0):
            print("Factory Seeder : Can't run factory, karena belum ada factory yang dibuat.")
            return
        
        db = SessionLocal()

        for factory in factories:
            
            factory_data = []

            for _ in range(self.count):

                factory_data.append(factory.build())

            db.add_all(factory_data)
            db.commit()

            print(f"Factory : {factory.__class__.__name__} have created with {self.count} times")

    def run_factory(self):

        if self.factory_name == "":
            return
        
        factory_path = f"app.factories.{ResourceName(self.factory_name).factory_file}"

        if importlib.util.find_spec(factory_path) is None:
            print(f"Error Factory : {self.factory} haven't created yet before")
            return
        
        factory_module = importlib.import_module(factory_path)
        factory_class_name = ResourceName(self.factory_name).factory_class
        factory_class = getattr(factory_module, factory_class_name)
        Factory = factory_class()

        db = SessionLocal()

        factory_data = []

        for _ in range(self.count):

            factory_data.append(Factory.build())

        db.add_all(factory_data)
        db.commit()

        print(f"Factory : {factory_class_name} have created with {self.count} times")