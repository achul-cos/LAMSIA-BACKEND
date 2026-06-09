from cli.flags.auto.schema_flag_auto import SchemaFlagAuto
from cli.flags.auto.repository_flag_auto import RepositoryFlagAuto

auto = RepositoryFlagAuto("pengasuh")
# auto = SchemaFlagAuto("pengasuh")

# print(auto.generate_schema_fields(auto.classify_fields()))

# print(auto.get_model_fields())

# print(auto.generate_create_schema())
# print(auto.generate_response_schema())

print(auto.generate_list_columns())

