from cli.generators.seeder_generator import SeederGenerator

class MakeSeederCommand:

    def __init__(self, resouce_name):
        self.resource_name = resouce_name

    def handle(self):
        generator = SeederGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Seeder Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")

    def handleAuto(self):
        generator = SeederGenerator(self.resource_name)

        file = generator.generateAuto()

        if file == False:
            return
        else:
            print(f"Seeder Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")      
            print(f"Using auto feature")  