# ------------------------------------------------------------------
# sensorresult_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /sensorresults yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /sensorresults akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.sensorresult_schema import SensorresultCreate, SensorresultResponse, SensorresultUpdate
from app.repositories.sensorresult_repository import SensorresultRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/sensorresults",
    tags=["Sensorresults"]
)

@router.post("/", response_model=SensorresultResponse)
def create_sensorresult(
    sensorresult_data: SensorresultCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.create(db, sensorresult_data)
    return RepositoryResponse

@router.get("/", response_model=list[SensorresultResponse])
def get_sensorresults(
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.get_all(db)
    return RepositoryResponse

@router.get("/{sensorresult_id:int}", response_model=SensorresultResponse)
def get_sensorresult(
    sensorresult_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.get_by_id(db, sensorresult_id)
    return RepositoryResponse

@router.put("/{sensorresult_id}", response_model=SensorresultResponse)
def update_put(
    sensorresult_id: int,
    sensorresult_data: SensorresultUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.update_put(db, sensorresult_id, sensorresult_data)
    return RepositoryResponse

@router.patch("/{sensorresult_id}", response_model=SensorresultResponse)
def update_patch(
    sensorresult_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.update_patch(db, sensorresult_id, payload)
    return RepositoryResponse

@router.delete("/{sensorresult_id}", response_model=SensorresultResponse)
def delete(
    sensorresult_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.delete(db, sensorresult_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = SensorresultRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[SensorresultResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = SensorresultRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[SensorresultResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return SensorresultRepository.where(db, query)