# ------------------------------------------------------------------
# kotakobat_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /kotakobats yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /kotakobats akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.kotakobat_schema import KotakobatCreate, KotakobatResponse, KotakobatUpdate
from app.repositories.kotakobat_repository import KotakobatRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/kotakobats",
    tags=["Kotakobats"]
)

@router.post("/", response_model=KotakobatResponse)
def create_kotakobat(
    kotakobat_data: KotakobatCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.create(db, kotakobat_data)
    return RepositoryResponse

@router.get("/", response_model=list[KotakobatResponse])
def get_kotakobats(
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.get_all(db)
    return RepositoryResponse

@router.get("/{kotakobat_id:int}", response_model=KotakobatResponse)
def get_kotakobat(
    kotakobat_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.get_by_id(db, kotakobat_id)
    return RepositoryResponse

@router.put("/{kotakobat_id}", response_model=KotakobatResponse)
def update_put(
    kotakobat_id: int,
    kotakobat_data: KotakobatUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.update_put(db, kotakobat_id, kotakobat_data)
    return RepositoryResponse

@router.patch("/{kotakobat_id}", response_model=KotakobatResponse)
def update_patch(
    kotakobat_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.update_patch(db, kotakobat_id, payload)
    return RepositoryResponse

@router.delete("/{kotakobat_id}", response_model=KotakobatResponse)
def delete(
    kotakobat_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.delete(db, kotakobat_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = KotakobatRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[KotakobatResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = KotakobatRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[KotakobatResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return KotakobatRepository.where(db, query)