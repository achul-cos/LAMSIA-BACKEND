from cli.utils.resource_name import ResourceName

class RouteTemplate:
    def __init__(self, route_name: str):
        self.route_name = route_name.lower()
        self.route_file_name = ResourceName(self.route_name).route_file
        self.route_class_name = ResourceName(self.route_name).class_name
        self.route_name_plural = ResourceName(self.route_name).table_name

    def build(self):

        return(
f'''# ------------------------------------------------------------------
# {self.route_file_name}.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /{self.route_name_plural} yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /{self.route_name_plural} akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.{self.route_name}_schema import {self.route_class_name}Create, {self.route_class_name}Response, {self.route_class_name}Update
from app.repositories.{self.route_name}_repository import {self.route_class_name}Repository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/{self.route_name_plural}",
    tags=["{self.route_name_plural.capitalize()}"]
)

@router.post("/", response_model={self.route_class_name}Response)
def create_{self.route_name}(
    {self.route_name}_data: {self.route_class_name}Create,
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.create(db, {self.route_name}_data)
    return RepositoryResponse

@router.get("/", response_model=list[{self.route_class_name}Response])
def get_{self.route_name_plural}(
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.get_all(db)
    return RepositoryResponse

@router.get("/{{{self.route_name}_id:int}}", response_model={self.route_class_name}Response)
def get_{self.route_name}(
    {self.route_name}_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.get_by_id(db, {self.route_name}_id)
    return RepositoryResponse

@router.put("/{{{self.route_name}_id}}", response_model={self.route_class_name}Response)
def update_put(
    {self.route_name}_id: int,
    {self.route_name}_data: {self.route_class_name}Update,
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.update_put(db, {self.route_name}_id, {self.route_name}_data)
    return RepositoryResponse

@router.patch("/{{{self.route_name}_id}}", response_model={self.route_class_name}Response)
def update_patch(
    {self.route_name}_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.update_patch(db, {self.route_name}_id, payload)
    return RepositoryResponse

@router.delete("/{{{self.route_name}_id}}", response_model={self.route_class_name}Response)
def delete(
    {self.route_name}_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.delete(db, {self.route_name}_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = {self.route_class_name}Repository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[{self.route_class_name}Response])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = {self.route_class_name}Repository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[{self.route_class_name}Response])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return {self.route_class_name}Repository.where(db, query)''')