from cli.generators.migration_generator import MigrationGenerator

generator = MigrationGenerator("user")

print(
    generator.generate()
)

# Untuk melakukan testing dapat menggunakan,
# python -m tests.test_migration_generator