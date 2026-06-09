from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator
from cli.flags.auto.schema_flag_auto import SchemaFlagAuto
from cli.template.schema_template import SchemaTemplate

class SchemaGenerator(BaseGenerator, SchemaFlagAuto):
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.resource = ResourceName(resource_name)
        self.auto = SchemaFlagAuto(resource_name)

    def generate(self):
        file_name = self.resource.schema_file
        file_path = Config.SCHEMA_PATH / file_name
        template = SchemaTemplate(self.resource_name).build()

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]
        
    def generateAuto(self):
        
        file_name = self.resource.schema_file
        file_path = Config.SCHEMA_PATH / file_name

        create_schema = self.auto.generate_create_schema()
        update_schema = self.auto.generate_update_schema()
        response_schema = self.auto.generate_response_schema()

        if create_schema is False or response_schema is False:
            print(f"System : Don't worry. We still made {file_name} for you.")
            return False
        
        template = SchemaTemplate(self.resource_name).build(schema_create=create_schema, schema_response=response_schema, schema_update=update_schema)

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]