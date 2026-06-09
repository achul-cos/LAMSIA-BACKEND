from cli.config.config import Config
from cli.utils.resource_name import ResourceName
from cli.generators.base_generator import BaseGenerator

class ModelGenerator(BaseGenerator):
    def __init__(self, resource_name):
        self.resource = ResourceName(resource_name)

    def generate(self):
        file_name = self.resource.model_file
        file_path = Config.MODEL_PATH / file_name
        template = (
f'''# ------------------------------------------------------------------
# {file_name}
# ------------------------------------------------------------------
# {file_name} digunakan untuk melakukan pemodelan class atau
# objek {self.resource.singular} pada sistem. Pemodelan mendefinisikan
# objek {self.resource.singular} memiliki atribut apa saja. 
# ------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from app.core.database import Base
from app.core.time import now

class {self.resource.class_name}(Base):
    """
    __tablename__ merupakan variabel yang mendefinisikan nama tabel dari objek {self.resource.singular}
    umumnya dituliskan dalam konsensi table name
    """
    __tablename__ = "{self.resource.table_name}"

    """
    Pada bagian ini yaitu atribut dari objek atau class tersebut yang tuliskan
    mengikuti format ORM atau tabel SQL, yang memiliki tipe data dan atribut
    tambahan lainya. Sebagai contoh: yaitu id, yang bertipe data integer
    dan sebagai primary key dari objek. 
    """

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(), default=now())
    updated_at = Column(DateTime(), default=now())    
            '''
        )

        writer = self.write_file(file_path, template) 

        if  writer == False:
            return False
        else:
            return [file_name, file_path]