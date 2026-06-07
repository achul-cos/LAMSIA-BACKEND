from app.core.database import SessionLocal

class BaseSeeder:
    def run(self):
        raise NotImplementedError("Seeder must implemented run()")