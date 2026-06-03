from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator

class SchemaGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.schema_file
        file_path = Config.SCHEMA_PATH / file_name
        template = (f'''
# ------------------------------------------------------------------
# {file_name}
# ------------------------------------------------------------------
# Kode {file_name} melakukan otorisasi kepada kode lainya pada sistem
# yang ingin menggunakan objek user. Otorisasi yang dilakukan
# seperti format data yang seharusnya diinput oleh pengguna saat akan
# menambahkan user baru, dan bagaimana sistem memberikan respon berupa
# data atribut objek User.
# ------------------------------------------------------------------
from pydantic import BaseModel

# {self.resource.class_name}Create mendefinisikan bahwa untuk melakukan interaksi create objek {self.resource.class_name}, membutuhkan data-data sesuai dengan {self.resource.model_file}
class {self.resource.class_name}Create(BaseModel):
    """
    Isi pada bagian ini, sesuai rancangan atribut pada data 
    {self.resource.model_file} dan sesuaikan juga dengan tipe datanya,
    tetapi tidak perlu menambahkan id nya, contoh:

    ------------------------------------------------------------------
    {self.resource.model_file}
    ------------------------------------------------------------------

    class {self.resource.class_name}(Base):
        __tablename__ = "{self.resource.table_name}"
        id = Column(Integer, primary_key=True, index=True)
        {self.resource.singular}Name = Column(String(100), nullable=False)
        {self.resource.singular}Password = Column(String(100), nullable=False)
    ------------------------------------------------------------------

    Maka pada kode {file_name}, seharusnya dituliskan sebagai berikut:

    class {self.resource.class_name}Create(BaseModel):
        {self.resource.singular}Name: str
        {self.resource.singular}Password: str
    """

# {self.resource.class_name}Response mendefinisikan bahwa untuk melakukan interaksi get atau SHOW pada objek {self.resource.class_name}, dapat menampilkan data-data sebagai berikut:
class {self.resource.class_name}UserResponse(BaseModel):

    """
    Berdasrkan dengan intruksi diatas, pada bagian ini dituliskan serupa
    dengan class {self.resource.class_name}Create. Tetapi pada bagian
    password itu disembunyikan demi keamanan, serta ditambahkan data
    id dengan tipe data int untuk dapat memberikan data int. Sebagai contoh.

    class {self.resource.class_name}UserResponse(BaseModel):
        id: int
        {self.resource.singular}Name: str
    """

    class Config:
        from_attribute = True
        ''')

        writer = self.write_file(file_path, template)

        if writer == False:
            return False
        else:
            return [file_name, file_path]