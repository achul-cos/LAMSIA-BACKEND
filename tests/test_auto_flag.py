from cli.flags.auto.migration_flag_auto import MigrationFlagAuto

resource_name = "pengasuh"

MigrationFlagAuto(resource_name).generate_migration_fields()