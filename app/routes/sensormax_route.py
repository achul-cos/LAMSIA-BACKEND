# ------------------------------------------------------------------
# sensormax_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /sensormaxes yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /sensormaxes akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.sensormax_schema import SensormaxCreate, SensormaxResponse, SensormaxUpdate
from app.repositories.sensormax_repository import SensormaxRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/sensormaxes",
    tags=["Sensormaxes"]
)

@router.post("/", response_model=SensormaxResponse)
def create_sensormax(
    sensormax_data: SensormaxCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.create(db, sensormax_data)
    return RepositoryResponse

@router.get("/", response_model=list[SensormaxResponse])
def get_sensormaxes(
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.get_all(db)
    return RepositoryResponse

@router.get("/{sensormax_id:int}", response_model=SensormaxResponse)
def get_sensormax(
    sensormax_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.get_by_id(db, sensormax_id)
    return RepositoryResponse

@router.put("/{sensormax_id}", response_model=SensormaxResponse)
def update_put(
    sensormax_id: int,
    sensormax_data: SensormaxUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.update_put(db, sensormax_id, sensormax_data)
    return RepositoryResponse

@router.patch("/{sensormax_id}", response_model=SensormaxResponse)
def update_patch(
    sensormax_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.update_patch(db, sensormax_id, payload)
    return RepositoryResponse

@router.delete("/{sensormax_id}", response_model=SensormaxResponse)
def delete(
    sensormax_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.delete(db, sensormax_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensormaxRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[SensormaxResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = SensormaxRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[SensormaxResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return SensormaxRepository.where(db, query)