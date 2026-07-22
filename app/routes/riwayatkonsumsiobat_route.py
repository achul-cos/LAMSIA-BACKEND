# ------------------------------------------------------------------
# riwayatkonsumsiobat_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /riwayatkonsumsiobats yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /riwayatkonsumsiobats akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.riwayatkonsumsiobat_schema import RiwayatkonsumsiobatCreate, RiwayatkonsumsiobatResponse, RiwayatkonsumsiobatUpdate
from app.repositories.riwayatkonsumsiobat_repository import RiwayatkonsumsiobatRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/riwayatkonsumsiobats",
    tags=["Riwayatkonsumsiobats"]
)

@router.post("/", response_model=RiwayatkonsumsiobatResponse)
def create_riwayatkonsumsiobat(
    riwayatkonsumsiobat_data: RiwayatkonsumsiobatCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.create(db, riwayatkonsumsiobat_data)
    return RepositoryResponse

@router.get("/", response_model=list[RiwayatkonsumsiobatResponse])
def get_riwayatkonsumsiobats(
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.get_all(db)
    return RepositoryResponse

@router.get("/{riwayatkonsumsiobat_id:int}", response_model=RiwayatkonsumsiobatResponse)
def get_riwayatkonsumsiobat(
    riwayatkonsumsiobat_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.get_by_id(db, riwayatkonsumsiobat_id)
    return RepositoryResponse

@router.put("/{riwayatkonsumsiobat_id}", response_model=RiwayatkonsumsiobatResponse)
def update_put(
    riwayatkonsumsiobat_id: int,
    riwayatkonsumsiobat_data: RiwayatkonsumsiobatUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.update_put(db, riwayatkonsumsiobat_id, riwayatkonsumsiobat_data)
    return RepositoryResponse

@router.patch("/{riwayatkonsumsiobat_id}", response_model=RiwayatkonsumsiobatResponse)
def update_patch(
    riwayatkonsumsiobat_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.update_patch(db, riwayatkonsumsiobat_id, payload)
    return RepositoryResponse

@router.delete("/{riwayatkonsumsiobat_id}", response_model=RiwayatkonsumsiobatResponse)
def delete(
    riwayatkonsumsiobat_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.delete(db, riwayatkonsumsiobat_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatkonsumsiobatRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[RiwayatkonsumsiobatResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = RiwayatkonsumsiobatRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[RiwayatkonsumsiobatResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return RiwayatkonsumsiobatRepository.where(db, query)
