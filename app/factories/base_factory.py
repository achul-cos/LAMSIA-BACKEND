from faker import Faker

fake = Faker()

class BaseFactory:
    def build(self):
        raise NotImplementedError("Factory must implemented build()")