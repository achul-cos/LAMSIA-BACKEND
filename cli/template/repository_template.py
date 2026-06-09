from cli.utils.resource_name import ResourceName

class RepositoryTemplate:
    def __init__(self, repository_name: str):
        self.repository_name = repository_name.lower()
        self.repository_file_name = ResourceName(self.repository_name).repository_file
        self.repository_class_name = ResourceName(self.repository_name).class_name
        self.repository_model_file = ResourceName(self.repository_name).model_file
        self.repository_model_class_name = ResourceName(self.repository_name).class_name
        self.repository_data_name = f"{self.repository_name}_data"
        self.repository_create_fields_default = (
        f"""            #atribut_1 = {self.repository_data_name}.atribut_1,
            #atribut_2 = {self.repository_data_name}.atribut_2,
            #atribut_3 = {self.repository_data_name}.atribut_3"""
        )
        self.repository_update_put_fields_default= (            
        f"""            #{self.repository_name}.atribute_1 = {self.repository_data_name}.atribut_1
            #{self.repository_name}.atribut_2 = {self.repository_data_name}.atribut_2
            #{self.repository_name}.atribut_3 = {self.repository_data_name}.atribut_3"""
        )

    def build(
        self,
        repository_create_fields: dict = {},   
    ):
        if repository_create_fields != {}:

            repository_create =""
            repository_update = ""
            
            i = 0
            j = 0

            # Create Fields

            while i < len(repository_create_fields["create_list"]):

                atr = str(repository_create_fields["create_list"][i])

                if i == len(repository_create_fields["create_list"]) - 1 :
                    repository_create += (f"""            {atr} = {self.repository_data_name}.{atr}""")
                    i += 1
                    continue

                repository_create += (f"""            {atr} = {self.repository_data_name}.{atr},
""")
                i += 1

            # Update Fields

            while j < len(repository_create_fields["update_list"]):

                atr = str(repository_create_fields["update_list"][j])

                if j == len(repository_create_fields["update_list"]) - 1 :
                    repository_update += (f"""            {self.repository_name}.{atr} = {self.repository_data_name}.{atr}""")
                    j += 1
                    continue

                repository_update += (f"""            {self.repository_name}.{atr} = {self.repository_data_name}.{atr}
""")
                j += 1

        return (
f'''# ------------------------------------------------------------------
# {self.repository_file_name}
# ------------------------------------------------------------------
# Kode ini mendefinisikan bagaimana sistem dapat menambahkan data
# {self.repository_class_name} berdasarkan format data {self.repository_name} yang diatur oleh {self.repository_name}_schema.py
# pada kelas {self.repository_class_name}Create; Serta kode ini menjelaskan bagaimana kode
# dapat mengambil semua data {self.repository_class_name} yang ada.
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.models.{self.repository_name}_model import {self.repository_class_name}
from app.schemas.{self.repository_name}_schema import {self.repository_class_name}Create, {self.repository_class_name}Update
from app.helper.query_parser import QueryParser
from app.core.time import now

class {self.repository_class_name}Repository:
    """
    fungsi create(), yaitu fungsi untuk menambahkan data {self.repository_name}
    dengan format data {self.repository_name} sesuai pada {self.repository_name}_schema.py, serta
    pada database (berdasarkan session yang diberikan).
    """
    @staticmethod
    def create(db: Session, {self.repository_data_name}: {self.repository_class_name}Create):
        {self.repository_name} = {self.repository_class_name}(
{repository_create if repository_create_fields != {} else self.repository_create_fields_default}
        )
        db.add({self.repository_name})
        db.commit()
        db.refresh({self.repository_name})
        return {self.repository_name}
    
    """
    fungsi get_all(), yaitu fungsi untuk mengambil seluruh data
    pada tabel {self.repository_name} yang berada pada database.
    """
    @staticmethod
    def get_all(db: Session):
        return db.query({self.repository_model_class_name}).all()

    @staticmethod
    def get_by_id(db: Session, {self.repository_name}_id: int):
        return(db.query({self.repository_model_class_name}).filter({self.repository_model_class_name}.id == {self.repository_name}_id).first())
    
    @staticmethod
    def update_put(db: Session, {self.repository_name}_id: int, {self.repository_data_name}: {self.repository_model_class_name}Update):
        {self.repository_name} = db.query({self.repository_model_class_name}).filter({self.repository_model_class_name}.id == {self.repository_name}_id).first()

        if not {self.repository_name}:
            return None

        else:
{repository_update if repository_create_fields != {} else self.repository_update_put_fields_default}
            {self.repository_name}.updated_at = now()

        db.commit()
        db.refresh({self.repository_name})
        return {self.repository_name}
    
    @staticmethod
    def update_patch(db: Session, {self.repository_name}_id:int, payload: dict):
        {self.repository_name} = db.query({self.repository_model_class_name}).filter({self.repository_model_class_name}.id == {self.repository_name}_id).first()

        if not {self.repository_name}:
            return None
        
        for key, value in payload.items():

            if not hasattr({self.repository_model_class_name}, key):
                continue

            setattr({self.repository_name}, key, value)

        {self.repository_name}.updated_at = now()

        db.commit()
        db.refresh({self.repository_name})
        return {self.repository_name}
    
    @staticmethod
    def delete(db: Session, {self.repository_name}_id: int):
        {self.repository_name} = db.query({self.repository_model_class_name}).filter({self.repository_model_class_name}.id == {self.repository_name}_id).first()

        if not {self.repository_name}:
            return None

        db.delete({self.repository_name})
        db.commit()
        return {self.repository_name}
    
    @staticmethod
    def delete_all(db: Session):
        db.query({self.repository_model_class_name}).delete(synchronize_session=False)

        db.commit()
        
        return {{
            "message": f"All {self.repository_model_class_name} deleted successfully"
        }}
    
    @staticmethod
    def filter(db: Session, **params):
        {self.repository_name} = db.query({self.repository_model_class_name})

        for key, value in params.items():
            if value is None:
                continue

            if hasattr({self.repository_model_class_name}, key):
                column = getattr({self.repository_model_class_name}, key)
                if "secret" in column.info:
                    continue

                {self.repository_name} = {self.repository_name}.filter(column == value)
        
        return {self.repository_name}.all()
    
    @staticmethod
    def where(db:Session, query):
        expression = QueryParser(query, {self.repository_model_class_name}).parse()
        
        if expression is None:
            return []        

        return db.query({self.repository_model_class_name}).filter(expression).all()''')