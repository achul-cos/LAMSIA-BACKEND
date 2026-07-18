from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.syntax import Syntax

class GenerateHelp():
    def __init__(self):
        self.console = Console()
    
    def generate(self):
        # Panel Title
        
        title = Panel(
            """           Fast API CLI Developments Tools         """,
            title="LAMSIA CLI",
            subtitle="v.0.1 Under Development",
        )

        # Description Project
        desc = (f"""\t\nLAMSIA CLI is Fast API CLI development tool. You can create python file or code just using cli command like laravel artisan experience. LAMSIA CLI actually just fun project from my main project is LAMSIA. So i took the name 'LAMSIA' from my main project to this project. Have fun and enjoy using this tool.""")

        # How To Use
        howToUseDesc = (f"""\tFor using LAMSIA CLI, you can accesing it by your terminal like command prompt or powershell (Recomendation) or etc. Most of LAMSIA CLI would like this:\n""")
        howToUseSchematic = Syntax("python lamsia.py [command] [command_value] --[command_flag]", "bash")
        howToUseExample = (f"""\nExample :\n""")
        howToUseExampleCommand = Syntax("python lamsia.py make:model user --auto", "bash")

        # Model Command
        modelCommand = (f'''
1.\t"Making Model"
\tcommand for making model file.
\n\tusage:
\t> python lamsia.py make:model (model_name) --(command-flags)
\n
''')

        self.console.print(Align.center(title))
        self.console.print(desc)
        self.console.rule("[bold blue]How To Use")
        self.console.print(howToUseDesc)
        self.console.print(howToUseSchematic)
        self.console.print(howToUseExample)
        self.console.print(howToUseExampleCommand)
        self.console.rule("[bold green]Commands")
        self.console.print(modelCommand)