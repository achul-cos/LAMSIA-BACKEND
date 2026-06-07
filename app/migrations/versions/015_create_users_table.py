
# ------------------------------------------------------------------
# 002_create_users_table.py
# ------------------------------------------------------------------
# 002_create_users_table.py yaitu kode yang mendefinisikan tabel migration dari
# model user_model.py. Kode ditulis dengan format ORM
# pewarisan dari class Base, yang terdiri dari nama column, tipe data,
# dan atribut lainya dari column tersebut
# ------------------------------------------------------------------

from app.migrations.schema_builder import Schema

def upgrade(engine):
    """
    Membuat tabel baru pada database atau jika tabelnya sudah ada,
    menambahkan column-column sesuai yang program pada fungsi ini.

    Parameters:
    engine (function) : fungsi creta_engine(database_url) dari modul SQLalchemy

    Function Schematic:
    Schema("<table_name>")\
        .id()\
        .<column_type_data>("<column_name>")\
        ...
    .build(engine)

    <table_name> (string)           : Nama table
    <column_type_data> (function)   : Tipe data dari column akan dibuat
    <column_name> (string)          : Nama column akan dibuat

    Example:
    Schema("test_table")\
        .id()\
        .int("atribute_1")\
        .string("atribute_2")\
    .build(engine)   
    """
    Schema("users")\
        .int("age")\
        .text("bio")\
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
    Schema("users").deleteColumns(engine, [
        'age',
        'bio'
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

    # Schema("users").deleteTable()