from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator
from cli.template.route_template import RouteTemplate

class RouteGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.route_file
        file_path = Config.ROUTE_PATH / file_name
        template = RouteTemplate(self.resource_name).build()

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path] 