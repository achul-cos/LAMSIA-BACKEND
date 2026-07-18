from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator
from cli.template.factory_template import FactoryTemplate
from cli.flags.auto.factory_flag_auto import FactoryFlagAuto

class FactoryGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.factory_file
        file_path = Config.FACTORY_PATH / f"{file_name}.py"
        template = FactoryTemplate(self.resource_name).build()

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]
        
    def generateAuto(self):
        file_name = self.resource.factory_file
        file_path = Config.FACTORY_PATH / f"{file_name}.py"

        auto_fields = FactoryFlagAuto(self.resource_name).generate_factory_fields()

        if (auto_fields != "" or isinstance(auto_fields, str) == False):
            template = FactoryTemplate(self.resource_name).build(auto_fields)
        
        else:
            template = FactoryTemplate(self.resource_name).build()
            print("Error Partial : Can't use auto feature, but we still made seeder for u")

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]