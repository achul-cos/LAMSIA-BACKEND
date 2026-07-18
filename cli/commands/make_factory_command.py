from cli.generators.factory_generator import FactoryGenerator

class MakeFactoryCommand:

    def  __init__(self, resource_name: str):
        self.resource_name = resource_name.lower()

    def handle(self):
        generator = FactoryGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Factory successful created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")

    def handleAuto(self):
        generator = FactoryGenerator(self.resource_name)

        file = generator.generateAuto()

        if file == False:
            return
        else:
            print(f"Factory Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")      
            print(f"Using auto feature")              