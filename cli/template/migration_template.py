from cli.utils.resource_name import ResourceName

class MigrationTemplate:
    def __init__(self, migration_name: str, migration_number: str=000):
        self.migration_name = migration_name
        self.migration_file_end_name = ResourceName(migration_name).migration_file
        self.migration_file_number = migration_number
        self.migration_file_name = f"{self.migration_file_number}_{self.migration_file_end_name}"
        self.migration_model = ResourceName(migration_name).class_name
        self.migration_table_name = ResourceName(migration_name).table_name

    def build(
        self, 
        migration_upgrade:str = (f".id()"),
        migration_downgrade:str = "",
        migration_fields:str = (f"        .id(){"\\"}")
        ):
        
        return (
f'''# ------------------------------------------------------------------
# {self.migration_file_name}.py
# ------------------------------------------------------------------
# Menjalankan migration pada model {self.migration_model} di database.
# Migration adalah membuat atau menghapus tabel suatu model.
# Tabel yang dibuat memiliki column-column yang disamakan dengan atribut
# model, bersamaan dengan tipe data dan meta data lainya
# ------------------------------------------------------------------

from app.migrations.schema_builder import Schema

def upgrade(engine):
    """
    Membuat tabel baru pada database atau jika tabelnya sudah ada,
    menambahkan column-column sesuai yang program pada fungsi ini.

    Parameters:
    engine (function) : fungsi creta_engine(database_url) dari modul SQLalchemy

    Function Schematic:
    Schema("<table_name>"){"\\"}
        .id(){"\\"}
        .<column_type_data>("<column_name>"){"\\"}
        ...
    .build(engine)

    <table_name> (string)           : Nama table
    <column_type_data> (function)   : Tipe data dari column akan dibuat
    <column_name> (string)          : Nama column akan dibuat

    Example:
    Schema("test_table"){"\\"}
        .id(){"\\"}
        .int("atribute_1"){"\\"}
        .string("atribute_2"){"\\"}
    .build(engine)   
    """
    Schema("{self.migration_table_name}"){"\\"}
{migration_fields}
    .build(engine)

def downgrade(engine):
    """
    (opsi 1) Menghapus column-column pada table database yang telah ada,

    Parameters:
    engine (variabel) : fungsi creata_engine(database_url) dari modul SQLalchemy

    Function Schematic:
    Schema("<table_name>").deleteColumns(engine, [
        '<table_column_1>',
        '<table_column_2>',
        ..
    ])

    <table_name> (string)       : Nama tabel
    <table_column_1> (string)   : Nama column yang akan dihapus

    Example:
    Schema("test_table").deleteColumns(engine, [
        'column_1',
        'column_2',
    ])
    """
    Schema("{self.migration_table_name}").deleteColumns(engine, [
        #'atrribute1',
        #'atribute2',
    ])

    """
    (opsi 2) Menghapus table dari database

    Parameters:
    engine (variabel) : fungsi creata_engine(database_url) dari modul SQLalchemy

    Function Schematic:
    Schema("<table_name>").deleteTable()

    <table_name> (string)   : Nama table yang akan dihapus

    Example:
    Schema("test_table").deleteTable()
    """

    # Schema("{self.migration_table_name}").deleteTable()''')