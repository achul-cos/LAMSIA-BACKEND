import inflect

engine = inflect.engine()

class ResourceName:
    def __init__(self, name):
        self.name = name.lower()
    
    @property
    def singular(self):
        return self.name
    
    @property
    def plural(self):
        return engine.plural(self.name)
    
    @property
    def class_name(self):
        return self.name.capitalize()
    
    @property
    def model_file(self):
        return f"{self.singular}_model.py"

    @property
    def schema_file(self):
        return f"{self.singular}_schema.py"
    
    @property
    def repository_file(self):
        return f"{self.singular}_repository.py"
    
    @property
    def route_file(self):
        return f"{self.singular}_route.py"
    
    @property
    def migration_file(self):
        return f"create_{self.plural}_table"