# ------------------------------------------------------------------
# 005_create_konsumsiobats_table.py
# ------------------------------------------------------------------
# Menjalankan migration pada model Konsumsiobat di database.
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
    Schema("konsumsiobats")\
        .id()\
        .foreign_key('id_obat', table='obats', column='id', nullable=False)\
        .foreign_key('id_kotakobat', table='kotakobats', column='id', nullable=False)\
        .datetime('waktu_minum', nullable=False)\
        .datetime('waktu_balikin', nullable=True)\
        .timestamps()\
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
    Schema("konsumsiobats").deleteColumns(engine, [
		'id',
		'id_obat',
		'id_kotakobat',
		'waktu_minum',
		'waktu_balikin',
		'created_at',
		'updated_at',
    ])

    """
    (opsi 2) Menghapus table dari database

    Parameters:
    engine (variabel) : fungsi creata_engine(database_url) dari modul SQLalchemy

    Function Schematic:
    Schema("<table_name>").deleteTable(engine)

    <table_name> (string)   : Nama table yang akan dihapus

    Example:
    Schema("test_table").deleteTable(engine)
    """

    Schema("konsumsiobats").deleteTable(engine)