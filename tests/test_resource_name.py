from cli.utils.resource_name import ResourceName

resource = ResourceName("user")

print("Singular:", resource.singular)
print("Plural:" ,resource.plural)
print("Class:", resource.class_name)
print("Model:", resource.model_file)
print("Schema:", resource.schema_file)
print("Repository:", resource.repository_file)
print("Migration:", resource.migration_file)

# Untuk melakukan testing dapat menggunakan,
# python -m tests.test_resource_name