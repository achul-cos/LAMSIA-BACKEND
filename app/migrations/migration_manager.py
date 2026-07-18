import os
import importlib
from sqlalchemy import inspect
from app.migrations.migration_model import Migration
from app.core.database import engine, SessionLocal, Base
from app.migrations.migration_model import Migration

MIGRATION_PATH = "app/migrations/versions"

def handle_migrations():
    ensure_migration_table_exist()
    run_migrations()

def ensure_migration_table_exist(engine=engine):
    inspector = inspect(engine)

    if not inspector.has_table("migrations"):
        print("Info : Migrations Table Haven't Created Before (Not Error If This Your First Migrate)")

        Migration.__table__.create(
            bind = engine,
            checkfirst = True
        )

        print("Success : Migrations Table Have Created")

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

def get_last_migrations(db):
    return db.query(Migration).order_by(Migration.id.desc()).first()

def rollback_last():
    db = SessionLocal()

    last = get_last_migrations(db)

    if not last:
        print("No any migrations to rollback")
        return
    
    migration_name = last.migration_name
    print(f"ROLLBACK : {migration_name}")

    # Import module the rollback migration
    module_path = f"app.migrations.versions.{migration_name}"
    module = importlib.import_module(module_path)

    # Jalankan downgrader pada rollback migration
    module.downgrade(engine)

    # Hapus migration ini pada table migrations, sebagai migration yang pernah atau telah dijalankan
    db.delete(last)
    db.commit()

    print(f"ROLLED BACK : {migration_name}")

def reset_migrations():
    db = SessionLocal()

    migrations = db.query(Migration).all()

    if not migrations:
        print("Info : Haven't migrate yet before")
        return
    
    for m in reversed(migrations):
        print(f"Rollback Migration : {m.migration_name}")

        migration_module_path = f"app.migrations.versions.{m.migration_name}"

        if importlib.util.find_spec(migration_module_path) is not None:

            module = importlib.import_module(migration_module_path)

            module.downgrade(engine)

        db.query(Migration).delete()

        db.commit()

        print("Success : All Migration Reset!")

def status():
    db = SessionLocal()
    
    applied_migrations = db.query(Migration).all()

    print("\nMigration Status:\n")

    for m in applied_migrations:

        print(f"{m.migration_name} : Already Migrated")

    print("\nDone\n")