from cli.flags.auto.seeder_flag_auto import SeederFlagAuto

a = SeederFlagAuto("pengasuh")

b = a.classify_fields()

c = a.generate_seeders_fields()

print(c)