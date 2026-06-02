from pathlib import Path

from cli.utils.resource_name import ResourceName

class MigrationGenerator:
    def __init__(self, resource_name):
        self.resource = ResourceName(resource_name)

    def get_next_number(self):
        migration_path = Path("app/migrations")
        migration_files = list(
            migration_path.glob("*.py")
        )
        return len(migration_files) + 1
    
    def generate(self):
        migration_number = str(self.get_next_number()).zfill(3)
        migration_name = self.resource.migration_file
        file_name = f"{migration_number}_{migration_name}.py"
        file_path = (Path("app/migrations")/file_name)
        template = (
            f'''
# ------------------------------------------------------------------
# {file_name}
# ------------------------------------------------------------------
# {file_name} yaitu kode yang mendefinisikan tabel migration dari
# model {self.resource.model_file}. Kode ditulis dengan format ORM
# pewarisan dari class Base, yang terdiri dari nama column, tipe data,
# dan atribut lainya dari column tersebut
# ------------------------------------------------------------------

"""
fungsi up(), yaitu fungsi yang diprogram untuk mendefinisikan column,
tipe data, atribut dan lainya terkait column tersebut. Kode ditulis
mengikuti rancangan dari model {self.resource.model_file} seharusnya.
"""
def up():
    pass
    
"""
fungsi down(), yaitu fungsi yang diprogram untuk menghapus column,
tipe data, atribut dan lainya terkait column tersebut secara
spesifik atau kesuluruhan tabel.
"""
def down():
    pass
        '''
            )
        with open(file_path, "w") as file:
            file.write(template)
        return file_name