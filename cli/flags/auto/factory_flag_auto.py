from importlib import import_module
from cli.utils.resource_name import ResourceName

class FactoryFlagAuto:

    def __init__(self, resource_name: str):
        self.resource = ResourceName(resource_name)

    def get_model_class(self):
        module_name = (
            f"app.models."
            f"{self.resource.model_file[:-3]}"
        )

        try:
            module = import_module(module_name)
        except Exception as e:
            print(f"Error Spatial : Can't run --auto feature. {module_name}.py haven't created yet.")
            print(f"System : {e}")
            return False
        
        model_class = getattr(module, self.resource.class_name)
        return model_class
    
    def get_model_columns(self):
        model = self.get_model_class()
        if model is False:
            return False
        model_column = model.__table__.columns
        return model_column
    
    def get_model_fields(self):
        fields = []
        model_columns = self.get_model_columns()

        if model_columns is False:
            return False

        for column in model_columns:

            fields.append(
                {
                    "name": column.name,
                    "type": type(column.type).__name__,
                    "primary_key": column.primary_key,
                    "secret": "secret" in column.info,
                    "nullable": column.nullable,
                }
            )
        
        return fields
    
    def classify_fields(self):
        key_data = []
        body_data = []
        nullable_data = []
        secret_data = []
        model_fields = self.get_model_fields()
        if model_fields is False:
            return False

        for field in model_fields:
            if field["primary_key"]:
                key_data.append(field)

            elif field["secret"]:
                secret_data.append(field)

            elif field["nullable"]:
                nullable_data.append(field)

            else:
                body_data.append(field)

        return [
            key_data, body_data, nullable_data, secret_data
        ]
    
    def map_python_type(self, sqlalchemy_type):
        mapping = {
            "Integer": "int",
            "String": "str",
            "Boolean": "bool",
            "Float": "float",
            "Enum": "Enum",
            "DateTime": "datetime"
        }

        return mapping.get(sqlalchemy_type, "str") 

    def generate_factory_fields(self):
        """
        Jika merujuk pada list self.classify_fields(), lisy akan berisi tiga anggota,
        self.classify_fields()[0] = Kelompok key_data,
        self.classify_fields()[1] = Kelompok body_data,
        self.classify_fields()[2] = Kelompok nullable_data,
        self.classify_fields()[3] = Kelompok secret_data,
        """
        fields = [self.classify_fields()[1], self.classify_fields()[3]]

        factory_fields = ""

        for f in fields:
            for a in f:
                if a["type"] == "String":
                    factory_fields += (f'                {a["name"]}="Lorem Ipsum",\n')
                elif a["type"] == "Integer":
                    factory_fields += (f'                {a["name"]}=0\n')
                else:
                    factory_fields += (f'                {a["name"]}=    # Tipe data {a["type"]}\n')
        
        return factory_fields           