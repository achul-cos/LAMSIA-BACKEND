from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator
from cli.template.repository_template import RepositoryTemplate
from cli.flags.auto.repository_flag_auto import RepositoryFlagAuto

class RepositoryGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.repository_file
        file_path = Config.REPOSITORY_PATH / file_name
        template = RepositoryTemplate(self.resource_name).build()

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path] 

    def generateAuto(self):
        file_name = self.resource.repository_file
        file_path = Config.REPOSITORY_PATH / file_name
        repository_auto = RepositoryFlagAuto(self.resource_name).generate_list_columns()
        template = RepositoryTemplate(self.resource_name).build(repository_create_fields=repository_auto)

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]         