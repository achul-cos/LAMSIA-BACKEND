# ------------------------------------------------------------------
# history_route.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /histories yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /histories akan didaftarkan pada main.py
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, HTTPException

from app.core.dependencies import get_db
from app.repositories.history_repository import HistoryRepository
from app.schemas.history_schema import HistoryResponse, MedicationHistoryResponse

router = APIRouter(
    prefix="/histories",
    tags=["Histories"]
)

@router.get("/", response_model=list[HistoryResponse])
def get_all_histories(
    db: Session = Depends(get_db)
):
    RepositoryResponse = HistoryRepository.get_all(db)
    return RepositoryResponse

@router.get("/medication", response_model=list[MedicationHistoryResponse])
def get_medication_history(
    db: Session = Depends(get_db)
): 
    return HistoryRepository.get_medication_history(db)

@router.get("/{history_id:int}", response_model=HistoryResponse)
def get_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = HistoryRepository.get_by_id(db, history_id)

    if RepositoryResponse is None:
        raise HTTPException(
            status_code=404,
            detail="History tidak ditemukan."
        )

    return RepositoryResponse

@router.delete("/{history_id}", response_model=HistoryResponse)
def delete(
    history_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = HistoryRepository.delete(db, history_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = HistoryRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[HistoryResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = HistoryRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[HistoryResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return HistoryRepository.where(db, query)