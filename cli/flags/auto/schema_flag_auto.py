from importlib import import_module
from cli.utils.resource_name import ResourceName

class SchemaFlagAuto:

    def __init__(self, resource_name):
        self.resource = ResourceName(resource_name)

    def get_model_class(self):
        module_name = (
            f"app.models."
            f"{self.resource.model_file[:-3]}"
        )
        try:
            module = import_module(module_name)
        except:
            print(f"Error Spatial : Can't run --auto feature. {module_name}.py haven't created yet.")
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
        secret_data = []
        model_fields = self.get_model_fields()
        if model_fields is False:
            return False

        for field in model_fields:
            if field["primary_key"]:
                key_data.append(field)
            elif field["secret"]:
                secret_data.append(field)
            else:
                body_data.append(field)

        return [
            key_data, body_data, secret_data
        ]
    
    def map_python_type(self, sqlalchemy_type):
        mapping = {
            "Integer": "int",
            "String": "str",
            "Boolean": "bool",
            "Float": "float",
        }

        return mapping.get(sqlalchemy_type, "str")
    
    def generate_schema_fields(self, fields):
        schema_fields = []

        """
        Jika merujuk pada list self.classify_fields(), lisy akan berisi tiga anggota,
        self.classify_fields()[0] = Kelompok key_data,
        self.classify_fields()[1] = Kelompok body_data,
        self.classify_fields()[2] = Kelompok secret_data,
        """
        for dataGroup in fields:
            data_field = []
            for data in dataGroup:
                python_type = self.map_python_type(data["type"])
                field = (f"{data["name"]}: {python_type}")
                data_field.append(field)
            schema_fields.append(data_field)
        
        return schema_fields
            
    def generate_create_schema(self):
        if self.classify_fields() is False:
            return False
        
        list_schema_fields = [
            self.generate_schema_fields(self.classify_fields())[1],
            self.generate_schema_fields(self.classify_fields())[2],
        ]

        schema_field = ""

        for groupList in list_schema_fields:
            for list in groupList:
                schema_field += f"""
    {str(list)}"""

        return schema_field

        # schema = (
        #     f"class {self.resource.class_name}Create(BaseModel):\n"
        #     +
        #     schema_field
        # )

        # return schema


    def generate_response_schema(self):
        if self.classify_fields() is False:
            return False
        
        list_schema_fields = [
            self.generate_schema_fields(self.classify_fields())[0],
            self.generate_schema_fields(self.classify_fields())[1],
        ]

        schema_field = ""

        for groupList in list_schema_fields:
            for list in groupList:
                schema_field += f"""
    {str(list)}"""

        return schema_field

    #     schema = (
    #         f"class {self.resource.class_name}Response(BaseModel):\n"
    #         +
    #         schema_field
    #         +
    #         f'''
    # class Config:
    #     from_attributes = True'''
    #     )

    #     return schema        