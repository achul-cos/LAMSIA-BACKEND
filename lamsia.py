from cli.commands.make_migration_command import MakeMigrationCommand
from cli.commands.make_model_command import MakeModalCommand
from cli.commands.make_schema_command import MakeSchemaCommand
from app.migrations.migration_manager import handle_migrations, rollback_last, reset_migrations, status

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

                model_command = MakeModalCommand(self.resource)
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