from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, Float, Text, Date, Time, JSON, Enum, text, inspect, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.sql import func
from sqlalchemy.schema import CreateColumn
from app.core.database import Base
from app.core.time import now
from datetime import datetime

class Schema:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    # ID
    def id(self):
        self.columns.append(
            Column("id", Integer, primary_key=True)
        )
        return self
    
    # Varchar (string)
    def string(self, name, length=255, nullable: bool = True, unique: bool = False, **kwargs):
        self.columns.append(
            Column(name, String(length=length), nullable=nullable, unique=unique, **kwargs)
        )
        return self
    
    # Text
    def text(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, Text, nullable=nullable, **kwargs)
        )
        return self
    
    # Integer
    def int(self, name, nullable: bool = True, unique: bool = False, **kwargs):
        self.columns.append(
            Column(name, Integer, nullable=nullable, unique=unique, **kwargs)
        )
        return self
    
    # Float
    def float(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, Float, nullable=nullable, **kwargs)
        )
        return self
     
    # Boolean
    def bool(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, Boolean, nullable=nullable, **kwargs)
        )
        return self
     
    # Date
    def date(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, Date, nullable=nullable, **kwargs)
        )
        return self
     
    # Time
    def time(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, Time, nullable=nullable, **kwargs)
        )
        return self
     
    # JSON
    def json(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, JSON, nullable=nullable, **kwargs)
        )
        return self
     
    # Enum
    def enum(self, name, values, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, Enum(*values), nullable=nullable, **kwargs)
        )
        return self
    
    # Double
    def double(self, name, nullable: bool = True, **kwargs):
        self.columns.append(
            Column(name, DOUBLE, nullable=nullable, **kwargs)
        )
        return self
     
    # Datetime
    def datetime(self, name, default = None, nullable: bool = True,**kwargs):
        self.columns.append(
            Column(name, DateTime, default=default, nullable=nullable, **kwargs)
        )
        return self

    # Timestamp
    def timestamps(self):
        self.columns.append(
            Column("created_at", DateTime, default=now())
        )
        self.columns.append(
            Column("updated_at", DateTime, default=now())
        )
        return self
    
    # Foreign key (int)
    def foreign_key(self, name: str, table: str, column: str = "id", nullable: bool = True):
        self.columns.append(
            Column(name, Integer, ForeignKey(f"{table}.{column}"), nullable=nullable)
        )
        return self


    def build(self, engine):
        # Memastikan apakah table migrations telah dibuat atau belum
        inspector = inspect(engine)

        if not inspector.has_table(self.table_name):
            table = Table(
                self.table_name,
                Base.metadata,
                *self.columns,
                extend_existing=True
            )

            table.create(bind=engine)
            print(f"Table Created: {self.table_name}")
            return

        # Jika table nya telah dibuat sebelumnya pada migrate sebelumnya,
        # Maka tambahkan column-column baru pada tablenya

        existed_columns = [col['name'] for col in inspector.get_columns(self.table_name)]

        for column in self.columns:

            if column.name not in existed_columns:

                query = f"ALTER TABLE {self.table_name} ADD COLUMN {CreateColumn(column).compile(engine)}"

                with engine.connect() as conn:
                    conn.execute(text(query))

                print(f"Success : Added {column.name} to {self.table_name}")

    def deleteColumns(self, engine, delete_columns: list = None):
        if not delete_columns:
            return
        
        inspector = inspect(engine)

        for col in delete_columns:

            if col not in inspector.get_columns(self.table_name):
                return
            else:
                continue
        
        drops = ", ".join([
            f"DROP COLUMN {column}" for column in delete_columns
        ])

        query_delete_columns = f"ALTER TABLE {self.table_name} {drops}"

        with engine.connect() as conn:
            conn.execute(text(query_delete_columns))
            conn.commit()

        print(f"Delete Column {tuple(delete_columns)} {self.table_name}")

    def deleteTable(self, engine):
        table = Table(
            self.table_name,
            Base.metadata,
            autoload_with=engine
        )

        table.drop(engine)
        print(f"Delete Table {self.table_name}")