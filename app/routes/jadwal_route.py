# ------------------------------------------------------------------
# jadwal_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /jadwals yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /jadwals akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session
from datetime import datetime,timedelta

from app.schemas.jadwal_schema import JadwalCreate, JadwalResponse, JadwalUpdate
from app.repositories.jadwal_repository import JadwalRepository
from app.repositories.konsumsiobat_repository import KonsumsiobatRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/jadwals",
    tags=["Jadwals"]
)

@router.post("/", response_model=JadwalResponse)
def create_jadwal(
    jadwal_data: JadwalCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = JadwalRepository.create(db, jadwal_data)
    return RepositoryResponse

@router.get("/", response_model=list[JadwalResponse])
def get_jadwals(
    db: Session = Depends(get_db)
):
    # Data jadwal + obat dari jadwal + riwayat jadwal dari jadwal
    jadwals = JadwalRepository.get_all(db)

    for jadwal in jadwals:

        riwayatjadwal = jadwal.riwayatjadwals
        id_obat = jadwal.id_obat
        
        for riwayat in riwayatjadwal:

            waktu_jadwal_konsumsi_obat = riwayat.waktu_riwayat
            waktu_jadwal_konsumsi_obat_terlambat = riwayat.waktu_riwayat + timedelta(minutes=45)

            riwayat_konsumsi_obat = KonsumsiobatRepository.where(query=f"((id_obat=={id_obat})&(waktu_minum_between={waktu_jadwal_konsumsi_obat},{waktu_jadwal_konsumsi_obat_terlambat}))", db=db)

            if len(riwayat_konsumsi_obat) >= 1:
                riwayat.is_terlambat = False
            else:
                riwayat.is_terlambat = True

            riwayat.riwayat_konsumsi = riwayat_konsumsi_obat


    return jadwals

@router.get("/{jadwal_id:int}", response_model=JadwalResponse)
def get_jadwal(
    jadwal_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = JadwalRepository.get_by_id(db, jadwal_id)
    return RepositoryResponse

@router.put("/{jadwal_id}", response_model=JadwalResponse)
def update_put(
    jadwal_id: int,
    jadwal_data: JadwalUpdate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = JadwalRepository.update_put(db, jadwal_id, jadwal_data)
    return RepositoryResponse

@router.patch("/{jadwal_id}", response_model=JadwalResponse)
def update_patch(
    jadwal_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = JadwalRepository.update_patch(db, jadwal_id, payload)
    return RepositoryResponse

@router.delete("/{jadwal_id}", response_model=JadwalResponse)
def delete(
    jadwal_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = JadwalRepository.delete(db, jadwal_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = JadwalRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[JadwalResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = JadwalRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[JadwalResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return JadwalRepository.where(db, query)