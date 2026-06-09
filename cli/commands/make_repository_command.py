from cli.generators.repository_generator import RepositoryGenerator

class MakeRepositoryCommand:

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def handle(self):
        generator = RepositoryGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Repository Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")

    def handleAuto(self):
        generator = RepositoryGenerator(self.resource_name)

        file = generator.generateAuto()

        if file == False:
            return
        else:
            print(f"Repository Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")
            
