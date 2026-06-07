from app.factories.base_factory import BaseFactory
from app.models.user_model import User
from faker import Faker

fake = Faker()

class UserFactory(BaseFactory):
    
    def build(self):
        return