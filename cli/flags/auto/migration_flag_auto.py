from importlib import import_module
from cli.utils.resource_name import ResourceName
import re

class MigrationFlagAuto:

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
                    "length": (str(column.type).split("(")[-1])[:-1],
                    "nullable": column.nullable,
                    "default": (((str(column.default)).split("(", maxsplit=1))[-1])[:-1],
                    "unique": column.unique,
                    "values": column.type
                }
            )
        
        # Testing
        # print(fields)

        return fields

    def generate_migration_fields(self):

        model_fields = self.get_model_fields()

        migration_fields = []

        for field in  model_fields:

            migration_field = ""

            if field["primary_key"] == True:
                migration_fields.append(".id()")
                continue

            length = ""
            nullable = ""
            unique = ""
            default = ""
            values = ""

            if field["length"] != "":

                try:
                    # Validasi bahwa nilai dari length itu berupa string
                    # dapat diubah menjadi angka
                    field_length = int(field["length"])
                    length = f", length={field_length}"
                except:
                    length = ""

            if field["nullable"] is not None:
                nullable = f", nullable={field["nullable"]}"

            if field["unique"] is not None:
                unique = f", unique={field["unique"]}"

            else:
                unique = ""

            if field["default"] is not None or \
                field["default"] != "" or \
                field["default"] != 'None' or \
                field["default"] != 'Non' or \
                field["type"] == 'DateTime' or \
                field["type"] == 'Date' or \
                field["type"] == 'Time':
                
                if field["default"] == "Non":
                    default = ""
                else:
                    if isinstance(field["default"], str) and (field["default"].startswith("'") or field["default"].startswith('"')):
                        field["default"] = field["default"].strip("'").strip('"')
                    
                    default = f", default='{field["default"]}'"
            else:
                default = ""
            
            if field["type"] == 'Enum':
                # enum_values = field["values"]
                # values = f", values={enum_values}"
                values = f", values=['enum1', 'enum2']"
                pass
            else:
                values = ""

            match field["type"]:

                case "Interger":

                    migration_field = f".int('{field["name"]}'{nullable}{unique}{default})"
                    migration_fields.append(migration_field)

                case "String":

                    migration_field = f".string('{field["name"]}'{length}{nullable}{unique}{default})"
                    migration_fields.append(migration_field)

                case "Enum":

                    migration_field = f".enum('{field["name"]}'{values}{nullable})"
                    migration_fields.append(migration_field)

                case "DateTime":
                    if field["name"] == 'created_at':
                        migration_field = f".timestamps()"
                        migration_fields.append(migration_field)

                    elif field["name"] == 'updated_at':
                        continue

                    else:
                        migration_field = f".datetime('{field["name"]}')"
            
                case _:

                    migration_field = f".string('{field["name"]}')"
                    migration_fields.append(migration_field)

        migration_fields_result = "\\\n".join("        " + column for column in migration_fields) + "\\"

        # For Testing
        # print(migration_fields_result)

        return migration_fields_result