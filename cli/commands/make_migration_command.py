from cli.generators.migration_generator import MigrationGenerator

class MakeMigrationCommand:

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def handle(self):
        generator = MigrationGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Migration Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")