import os
import importlib
from app.core.database import engine, SessionLocal
from app.migrations.migration_model import Migration

MIGRATION_PATH = "app/migrations/versions"

def get_applied_migrations(db):
    return {m.migration_name for m in db.query(Migration).all()}

def run_migrations():
    db = SessionLocal()

    applied_migrations = get_applied_migrations(db)

    files = sorted(os.listdir(MIGRATION_PATH))

    for file in files:
        if not file.endswith('.py'):
            continue

        migration_name = file.replace('.py', '')

        if migration_name in applied_migrations:
            print(f"SKIP : {migration_name}")
            continue

        print(f"RUN : {migration_name}")

        # Import File Migration
        module_path = f"app.migrations.versions.{migration_name}"
        module = importlib.import_module(module_path)

        module.upgrade(engine)

        new_migration = Migration(
            migration_name=migration_name
        )

        db.add(new_migration)
        db.commit()

        print(f"Done! : {migration_name}")