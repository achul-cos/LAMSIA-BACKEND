from cli.generators.route_generator import RouteGenerator

class MakeRouteCommand:

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def handle(self):
        generator = RouteGenerator(self.resource_name)

        file = generator.generate()

        if file == False:
            return
        else:
            print(f"Route Successful Created : {file[0]}")
            print(f"{file[0]} Path : {file[1]}")
