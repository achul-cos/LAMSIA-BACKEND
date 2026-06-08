from app.factories.base_factory import BaseFactory
from app.models.user_model import User
from faker import Faker

fake = Faker('id_ID')

class UserFactory(BaseFactory):
    
    def build(self):
        return User(
            username=fake.user_name(),
            telephone=fake.phone_number(),
            password=fake.password(length=10)
        )