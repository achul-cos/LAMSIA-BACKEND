from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator
from cli.template.seeder_template import SeederTemplate
from cli.flags.auto.seeder_flag_auto import SeederFlagAuto

class SeederGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.seeder_file
        file_path = Config.SEEDER_PATH / f"{file_name}.py"
        template = SeederTemplate(self.resource_name).build()

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]
        
    def generateAuto(self):
        file_name = self.resource.seeder_file
        file_path = Config.SEEDER_PATH / f"{file_name}.py"

        auto_fields = SeederFlagAuto(self.resource_name).generate_seeders_fields()

        if (auto_fields != "" or isinstance(auto_fields, str) == False):
            template = SeederTemplate(self.resource_name).build(auto_fields)

        else:
            template = SeederTemplate(self.resource_name).build()
            print("Error Partial : Can't use auto feature, but we still made seeder for u")
        
        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]
