import os
from datetime import datetime
from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator
from cli.template.migration_template import MigrationTemplate

class MigrationGenerator(BaseGenerator):
    def __init__(self, resource_name, migration_fields:str = ""):
        self.resource_name = resource_name
        self.resource = ResourceName(resource_name)
        self.migration_fields = migration_fields

    def get_latest_number(self):
        migration_path = Config.MIGRATION_PATH

        files = os.listdir(migration_path)

        migration_versios_numbers = []

        for file in files:
            if file.endswith('.py') and file[0:3].isdigit():
                migration_versios_numbers.append(int(file[0:3]))

        if not migration_versios_numbers:
            return 0
        
        return max(migration_versios_numbers)
    
    def generate(self):
        next_migration_version_number = self.get_latest_number() + 1

        migration_name = self.resource.migration_file

        migration_number = f"{next_migration_version_number:03d}"

        file_name = f"{migration_number}_{migration_name}.py"

        file_path = Config.MIGRATION_PATH / file_name

        if self.migration_fields == "":
            template = MigrationTemplate(self.resource_name, migration_number).build()

        else:
            template = MigrationTemplate(self.resource_name, migration_number).build(migration_fields=self.migration_fields)
        
        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]