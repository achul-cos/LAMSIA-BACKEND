from cli.commands.make_migration_command import MakeMigrationCommand
from cli.commands.make_model_command import MakeModelCommand
from cli.commands.make_schema_command import MakeSchemaCommand
from cli.utils.resource_name import ResourceName
from app.migrations.migration_manager import handle_migrations, rollback_last, reset_migrations, status
from app.seeders.seeder_runner import run_seeder, run_seeders
from app.factories.factory_seeder import FactorySeeder

import sys

class Lamsia:

    def __init__(self):
        if len(sys.argv) > 1:
            self.command = sys.argv[1].lower()
        else:
            print("Error : There's No Any Command")
            sys.exit()

        if len(sys.argv) > 2:
            if sys.argv[2].startswith("--") or sys.argv[2].startswith("-"):
                self.resource = ""
            else:
                self.resource = sys.argv[2]
        else:
            self.resource = ""

        self.flags = []

        for arg in sys.argv[2:]:
            if arg.startswith("--"):
                self.flags.append(arg)

    def has_flag(self, flag):
        return flag in self.flags

    def handle(self):
        match self.command:
            case "make:migration":
                # For testing purpose
                # print(f"This migation command for {resource}")   

                """
                Migration Command Schematic:
                > python lamsia.py make:migration [name_migration]

                this is version 0.1 (may there will have update on the next version) 
                """

                if self.resource == "":
                    print(f"Error : Migration Command Scematic Invalid.")
                    print(f"python lamsia.py make:migration [name_migration]")
                    print("You didn't input any [name_migration]")
                    sys.exit()

                if self.has_flag("--auto"):
                    migration_command = MakeMigrationCommand(self.resource)
                    migration_command.handleAuto() 
                else:
                    migration_command = MakeMigrationCommand(self.resource)
                    migration_command.handle()

            case "make:model":
                # For Testing Purpose
                # print(f"This model command for {self.resource}")

                """
                Model Command Schematic:
                > python lamsia.py make:model [name_model]

                this is version 0.1
                """

                if self.resource == "":
                    print(f"Error : Model Command Scematic Invalid.")
                    print(f"python lamsia.py make:model [name_model]")
                    print("You didn't input any [name_model]")  
                    sys.exit()

                model_command = MakeModelCommand(self.resource)
                model_command.handle()                  

            case "make:schema":
                # For Testing Purpose
                # print(f"This schema command for {self.resource}")

                """
                Schema Command Schematic:

                > python lamsia.py make:schema [name_schema] --[flags]

                this is version 0.1
                """

                if self.resource == "":
                    print(f"Error : Schema Command Scematic Invalid.")
                    print(f"python lamsia.py make:schema [name_schema]")
                    print("You didn't input any [name_schema]")  
                    sys.exit()

                if self.has_flag("--auto"):
                    schema_command = MakeSchemaCommand(self.resource)
                    schema_command.handleAuto() 
                else:
                    schema_command = MakeSchemaCommand(self.resource)
                    schema_command.handle()                          

            case "make:repository":
                print(f"This repository command for {self.resource}")

            case "make:route":
                print(f"This route command for {self.resource}")

            case "make:resource":
                print(f"This migration, model, schema, repository, and route command for {self.resource}")

            case "migrate":

                """
                Migrate Command Schematic:

                > python lamsia.py migrate --[flags]

                this is version 0.1
                """

                handle_migrations()

            case "migrate:reset":
                """
                Migration Reset Command Schematic:

                > python lamsia.py migrate:reset --[flags]

                this is version 0.1
                """

                reset_migrations()

            case "migrate:refresh":
                """
                Migration Refresh Command Schematic:

                > python lamsia.py migrate:refresh --[flags]

                this is version 0.1
                """

                print("System Reset Migration")
                reset_migrations()

                print("System Migrating Migration")
                handle_migrations()

            case "migrate:status":
                """
                Migration Status Command Schematic:

                > python lamsia.py migrate:status --[flags]

                this is version 0.1
                """

                status()

            case "rollback":
                """
                Rollback Command Schematic:

                > python lamsia.py rollback --[flags]

                this is version 0.1
                """

                rollback_last()

            case "seed":
                """
                Seeder Command Schematic:

                > python lamsia.py seed [seeder_name] --flag[]
                """

                if self.resource == "":
                    run_seeders()

                if self.resource != "":
                    run_seeder(self.resource)

            case "factory":
                """
                Factory Command Schematic:

                > python lamsia.py factory [factory_name] --[flags]

                [flags]:

                --count=[quantity_data] : Berapa jumlah factory yang ingin dibuat

                this is version 0.1
                """
                if any(flag.startswith("--count") for flag in self.flags):

                    for flag in self.flags:

                        if flag.startswith("--count="):
                            count = (flag.split("="))[1]

                            try:
                                count = int(count)

                                if self.resource == "":
                                    FactorySeeder(count=count).run()

                                if self.resource != "":
                                    FactorySeeder(self.resource, count=count).run_factory()                            

                            except:
                                print(f"Spatial Error : Count flag value is not valid. {count} is not number")
                                print(f"Error Handler : Still Excuted the command,")

                                if self.resource == "":
                                    print(f"> python lamsia.py factory")
                                    FactorySeeder().run()
                                    break

                                if self.resource != "":
                                    print(f"> python lamsia.py factory {self.resource}")
                                    FactorySeeder(factory_name=self.resource).run_factory()
                                    break

                        else:
                            continue

                    sys.exit()

                else:
                    if self.resource == "":
                        FactorySeeder().run()

                    if self.resource != "":
                        FactorySeeder(factory_name=self.resource).run_factory()   

                    sys.exit()

            case "make:resource":
                """
                Resource Generate Command Schematic:

                > py lamsia.py make:resource [resource_name] --[flags]

                this is version 0.1
                """
                
                if self.resource == "":
                    print(f"Error : Resource Command Scematic Invalid.")
                    print(f"python lamsia.py make:resource [resouce_name]")
                    print("You didn't input any [resouce_name]")  
                    sys.exit()

                # Make Model
                model_command = MakeModalCommand(self.resource)
                model_command.handle() 

                # Make Schema
                schema_command = MakeSchemaCommand(self.resource)
                schema_command.handle()

                # Make Repository
                                                  

            case "help":
                print(
                    f"""
LAMSIA CLI Tool for FASTAPI Project
version : v0.1 (development version)
author : achul.cos https://github.com/achul-cos

Command :

    >py lamsia.py make:migration [migration_name]       // Create migration file command

    >py lamsia.py make:model [model_name]               // Create model file command

    >py lamsia.py make:schema [schemma_name]            // Create schema file command

    >py lamsia.py make:repository [repository_name]     // Create repository file command

    >py lamsia.py make:route [route_name]               // Create route file command

    >py lamsia.py make:resource [resource_name]         // Create migration, model, schema, repository and route file with same name at once

❤︎ Make FastAPI Project, like you make Laravel API Project❤︎   
                    """
                    )
                           
            case _:
                print("Error : Invalid Command. Want to see help? Use: \n")
                print("python lamsia.py help")

def main():
    
    lamsia = Lamsia()

    lamsia.handle()

if __name__ == "__main__":
    main()