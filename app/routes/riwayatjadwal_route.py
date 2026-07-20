# ------------------------------------------------------------------
# riwayatjadwal_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /riwayatjadwals yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /riwayatjadwals akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.riwayatjadwal_schema import RiwayatjadwalCreate, RiwayatjadwalResponse, RiwayatjadwalUpdate
from app.repositories.riwayatjadwal_repository import RiwayatjadwalRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/riwayatjadwals",
    tags=["Riwayatjadwals"]
)

@router.post("/", response_model=RiwayatjadwalResponse)
def create_riwayatjadwal(
    riwayatjadwal_data: RiwayatjadwalCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatjadwalRepository.create(db, riwayatjadwal_data)
    return RepositoryResponse

@router.get("/", response_model=list[RiwayatjadwalResponse])
def get_riwayatjadwals(
    db: Session = Depends(get_db)
):
    riwayatjadwal = RiwayatjadwalRepository.get_all(db)
    
    return riwayatjadwal

@router.get("/{riwayatjadwal_id:int}", response_model=RiwayatjadwalResponse)
def get_riwayatjadwal(
    riwayatjadwal_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatjadwalRepository.get_by_id(db, riwayatjadwal_id)
    return RepositoryResponse

@router.put("/{riwayatjadwal_id}", response_model=RiwayatjadwalResponse)
def update_put(
    riwayatjadwal_id: int,
    riwayatjadwal_data: RiwayatjadwalUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatjadwalRepository.update_put(db, riwayatjadwal_id, riwayatjadwal_data)
    return RepositoryResponse

@router.patch("/{riwayatjadwal_id}", response_model=RiwayatjadwalResponse)
def update_patch(
    riwayatjadwal_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatjadwalRepository.update_patch(db, riwayatjadwal_id, payload)
    return RepositoryResponse

@router.delete("/{riwayatjadwal_id}", response_model=RiwayatjadwalResponse)
def delete(
    riwayatjadwal_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatjadwalRepository.delete(db, riwayatjadwal_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = RiwayatjadwalRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[RiwayatjadwalResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = RiwayatjadwalRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[RiwayatjadwalResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return RiwayatjadwalRepository.where(db, query)