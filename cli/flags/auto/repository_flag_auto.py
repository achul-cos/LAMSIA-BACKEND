from importlib import import_module
from cli.utils.resource_name import ResourceName
import re

class RepositoryFlagAuto:

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

        if model_columns is None or model_columns == []:
            return False

        for column in model_columns:

            fields.append(
                {
                    "name": column.name,
                    "type": type(column.type).__name__,
                    "primary_key": column.primary_key,
                    "secret": "secret" in column.info,
                    "length": (str(column.type).split("(")[-1])[:-1],
                    "nullable": column.nullable,
                    "default": (((str(column.default)).split("(", maxsplit=1))[-1])[:-1],
                    "unique": column.unique,
                    "values": column.type
                }
            )

        return fields
    
    def generate_list_columns(self):

        model_fields = self.get_model_fields()

        create_list_columns = []

        update_list_columns = []

        if model_fields is None or model_fields == []:
            return False
        
        for column in model_fields:

            if column['name'] == '' or \
            column['name'] == 'created_at' or \
            column['name'] == 'updated_at' or \
            column['primary_key'] == True:
                continue

            update_list_columns.append(column['name'])

            if column['nullable'] != True:
                create_list_columns.append(column['name'])

        return {
            "create_list": create_list_columns,
            "update_list": update_list_columns
        }

