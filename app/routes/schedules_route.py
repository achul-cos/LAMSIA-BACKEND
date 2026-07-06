# ------------------------------------------------------------------
# schedules_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /schedule yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /schedule akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.schemas.schedules_schema import SchedulesCreate, SchedulesResponse, SchedulesUpdate
from app.repositories.schedules_repository import SchedulesRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"]
)

@router.post("/", response_model=SchedulesResponse)
def create_schedules(
    schedules_data: SchedulesCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.create(db, schedules_data)
    return RepositoryResponse

@router.get("/", response_model=list[SchedulesResponse])
def get_schedule(
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.get_all(db)
    return RepositoryResponse

@router.get("/{schedules_id:int}", response_model=SchedulesResponse)
def get_schedules(
    schedules_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.get_by_id(db, schedules_id)
    return RepositoryResponse

@router.put("/{schedules_id}", response_model=SchedulesResponse)
def update_put(
    schedules_id: int,
    schedules_data: SchedulesUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.update_put(db, schedules_id, schedules_data)
    return RepositoryResponse

@router.patch("/{schedules_id}", response_model=SchedulesResponse)
def update_patch(
    schedules_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.update_patch(db, schedules_id, payload)
    return RepositoryResponse

@router.delete("/{schedules_id}", response_model=SchedulesResponse)
def delete(
    schedules_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.delete(db, schedules_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = SchedulesRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[SchedulesResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = SchedulesRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[SchedulesResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return SchedulesRepository.where(db, query)