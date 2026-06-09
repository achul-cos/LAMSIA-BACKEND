# ------------------------------------------------------------------
# pengasuh_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /pengasuhs yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /pengasuhs akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.pengasuh_schema import PengasuhCreate, PengasuhResponse, PengasuhUpdate
from app.repositories.pengasuh_repository import PengasuhRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/pengasuhs",
    tags=["Pengasuhs"]
)

@router.post("/", response_model=PengasuhResponse)
def create_pengasuh(
    pengasuh_data: PengasuhCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.create(db, pengasuh_data)
    return RepositoryResponse

@router.get("/", response_model=list[PengasuhResponse])
def get_pengasuhs(
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.get_all(db)
    return RepositoryResponse

@router.get("/{pengasuh_id:int}", response_model=PengasuhResponse)
def get_pengasuh(
    pengasuh_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.get_by_id(db, pengasuh_id)
    return RepositoryResponse

@router.put("/{pengasuh_id}", response_model=PengasuhResponse)
def update_put(
    pengasuh_id: int,
    pengasuh_data: PengasuhUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.update_put(db, pengasuh_id, pengasuh_data)
    return RepositoryResponse

@router.patch("/{pengasuh_id}", response_model=PengasuhResponse)
def update_patch(
    pengasuh_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.update_patch(db, pengasuh_id, payload)
    return RepositoryResponse

@router.delete("/{pengasuh_id}", response_model=PengasuhResponse)
def delete(
    pengasuh_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.delete(db, pengasuh_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = PengasuhRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[PengasuhResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = PengasuhRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[PengasuhResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return PengasuhRepository.where(db, query)