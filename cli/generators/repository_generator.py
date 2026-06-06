from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator

class RepositoryGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.repository_file
        file_path = Config.REPOSITORY_PATH / file_name
        template = ()