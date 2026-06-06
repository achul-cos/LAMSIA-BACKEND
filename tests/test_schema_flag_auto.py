from cli.flags.auto.schema_flag_auto import SchemaFlagAuto

auto = SchemaFlagAuto("user")

# print(auto.generate_schema_fields(auto.classify_fields()))

# print(auto.get_model_fields())

print(auto.generate_create_schema())
print(auto.generate_response_schema())