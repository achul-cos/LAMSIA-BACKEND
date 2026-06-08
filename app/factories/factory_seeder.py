from app.core.database import SessionLocal
from app.factories.user_factory import UserFactory
from cli.utils.resource_name import ResourceName
import importlib

class FactorySeeder:
    def __init__(self, factory_name: str = "", count: int = 10):
        self.factory_name = factory_name
        self.count = count

    def run(self):

        db = SessionLocal()

        FactorySeeder = [
            UserFactory()
        ]

        for factory in FactorySeeder:

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