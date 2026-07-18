
# ------------------------------------------------------------------
# sensormax_factory.py
# ------------------------------------------------------------------
# Kode ini menjalankan fungsi factory. Factory adalah sebuah kode
# yang merancang sebuah objek pada suatu model yang ditentukan, untuk 
# dapat dibuat secara bulk atau bersamaan tanpa harus membuat satu per satu.
# Kode factory adalah rancangan objek tersebut. Pada umumny factory sering
# menggunakan faker untuk membuat data-data dummy.
# ------------------------------------------------------------------

from app.factories.base_factory import BaseFactory
from app.models.sensormax_model import Sensormax
from faker import Faker

# Menggunakan Faker sebagai pembuat data palsu dengan konfigurasi di parameternya ('id_ID')
# Untuk lokasilisasi data dummy yang dia dapatkan.
fake = Faker('id_ID')

class SensormaxFactory(BaseFactory):
    """
    Merancangan objek model yang akan dibuat secara bulk atau bersamaan,
    pada variabel atau properti yang dimiliki oleh objek nantinya,
    dengan bantuan faker

    function schematic:
    from app.models.<model_file> import <model_class>

    def build(self):
        return <model_name>(
            <model_column_1>=fake.pystr(min_chars=10, max_chars=20),    # untuk data string
            <model_column_2>=fake.fake.random_int(min=100, max=500),    # untuk data integer
            <model_column_3>=fake.password(length=10),                  # untuk data berupa password
            <model_column_4>=fake.user_name(),                          # untuk data berupa username
            <model_column_5>=fake.phone_number(),                       # untuk data phone number
            <model_column_6>=<model_column_6_value_default>             # untuk data default
        )

    <model_file> (file)             : nama file dari model seeder
    <model_class> (object)          : model seeder
    <model_column>                  : column atau data atau variabel pada model
    <model_column_value_default>    : nilai default pada suatu column objek model yang di rancang pada factory

    Example:
    from app.models.user_model import User

    def build(self):
        return User(
            username=fake.user_name(),
            telephone=fake.phone_number(),
            password=fake.password(length=10)
        )    
    """
    
    def build(self):
        return Sensormax(
            # Isi Disini
                hr=0,
                sp=0,
                ir=0,
                red=0,
            
        )
