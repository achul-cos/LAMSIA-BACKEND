# ------------------------------------------------------------------
# obat_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /obats yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /obats akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.schemas.obat_schema import ObatCreate, ObatResponse, ObatUpdate, ObatListResponse
from app.repositories.obat_repository import ObatRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/obats",
    tags=["Obats"]
)

@router.post("/", response_model=ObatResponse)
def create_obat(
    obat_data: ObatCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.create(db, obat_data)
    return RepositoryResponse

@router.get("/", response_model=list[ObatListResponse])
def get_obats(
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.get_all(db)
    return RepositoryResponse

@router.get("/{obat_id:int}", response_model=ObatResponse)
def get_obat(
    obat_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.get_by_id(db, obat_id)
    return RepositoryResponse

@router.put("/{obat_id}", response_model=ObatResponse)
def update_put(
    obat_id: int,
    obat_data: ObatUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.update_put(db, obat_id, obat_data)
    return RepositoryResponse

@router.patch("/{obat_id}", response_model=ObatResponse)
def update_patch(
    obat_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.update_patch(db, obat_id, payload)
    return RepositoryResponse

@router.delete("/{obat_id}", response_model=ObatResponse)
def delete(
    obat_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.delete(db, obat_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = ObatRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[ObatResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = ObatRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[ObatResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return ObatRepository.where(db, query)