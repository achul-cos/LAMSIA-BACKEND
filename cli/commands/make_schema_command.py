from cli.generators.schema_generator import SchemaGenerator

class MakeSchemaCommand:

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def handle(self):
        generator = SchemaGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Schema Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")

    def handleAuto(self):
        generator = SchemaGenerator(self.resource_name)

        file = generator.generateAuto()

        if file is False:
            self.handle()
        else:
            print(f"Schema Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")
            print(f"Using auto features")