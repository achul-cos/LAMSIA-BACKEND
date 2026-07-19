from cli.flags.auto.migration_flag_auto import MigrationFlagAuto

auto = MigrationFlagAuto("jadwal")

# print(auto.get_model_fields())
print(auto.generate_migration_fields())


