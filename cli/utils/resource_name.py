import inflect

engine = inflect.engine()

class ResourceName:
    def __init__(self, name):
        self.name = name.lower()
    
    @property
    def singular(self):
        return self.name
    
    @property
    def table_name(self):
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
        return f"create_{self.table_name}_table"
    
    @property
    def seeder_file(self):
        return f"{self.singular}_seeder"
    
    @property
    def seeder_class(self):
        return f"{self.class_name}Seeder"
    
    @property
    def factory_file(self):
        return f"{self.singular}_factory"
    
    @property
    def factory_class(self):
        return f"{self.class_name}Factory"