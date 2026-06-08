from cli.generators.model_generator import ModelGenerator

class MakeModelCommand:

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def handle(self):
        generator = ModelGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Model Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")

    # def handleAuto(self):
    #     pass