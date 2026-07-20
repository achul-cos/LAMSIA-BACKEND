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
from datetime import timedelta

from app.schemas.riwayatjadwal_schema import RiwayatjadwalCreate, RiwayatjadwalResponse, RiwayatjadwalUpdate, RiwayatjadwalResponseWithKonsumsiObat
from app.schemas.konsumsiobat_schema import KonsumsiobatResponse
from app.repositories.riwayatjadwal_repository import RiwayatjadwalRepository
from app.repositories.konsumsiobat_repository import KonsumsiobatRepository
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

@router.get("/", response_model=list[RiwayatjadwalResponseWithKonsumsiObat])
def get_riwayatjadwals(
    db: Session = Depends(get_db)
):
    riwayatjadwal = RiwayatjadwalRepository.get_all(db)
    
    urutan_riwayat_jadwal = 0

    # Iterasi versi kedua
    while urutan_riwayat_jadwal < len(riwayatjadwal):
        
        # buat variabel riwayat berdasarkan urutan iterasinya
        riwayat : RiwayatjadwalResponseWithKonsumsiObat = riwayatjadwal[urutan_riwayat_jadwal]

        id_obat = riwayat.jadwals.obat.id

        riwayat.id_obat = id_obat

        # buat variabel riwayat 
        if urutan_riwayat_jadwal + 1 < len(riwayatjadwal):
            riwayat_selanjutnya : RiwayatjadwalResponseWithKonsumsiObat = riwayatjadwal[urutan_riwayat_jadwal + 1]
        else:
            riwayat_selanjutnya = riwayat

        # buat variabel waktu konsumsi obat pada jadwal yang di ambil dari riwayat
        waktu_konsumsi_obat_pada_jadwal = riwayat.waktu_riwayat
        waktu_konsumsi_obat_pada_jadwal_selanjutnya = riwayat_selanjutnya.waktu_riwayat

        # tentukan tenggat terlambat waktu konsumsi obat berdasarkan jadwal
        waktu_konsumsi_obat_terlambat_pada_jadwal = waktu_konsumsi_obat_pada_jadwal + timedelta(minutes=45)
        waktu_konsumsi_obat_terlambat_pada_jadwal_selanjutnya = waktu_konsumsi_obat_pada_jadwal_selanjutnya + timedelta(minutes=45)

        # Lalu cari riwayat konsumsi obat pada rentang waktu_konsumsi_obat_pada_jadwal hingga waktu_konsumsi_obat_terlambat_pada_jadwal
        riwayat_konsumsi_obat = KonsumsiobatRepository.where(query=f"((id_obat=={id_obat})&(waktu_minum_between={waktu_konsumsi_obat_pada_jadwal},{waktu_konsumsi_obat_terlambat_pada_jadwal}))", db=db)

        # Jika ada maka berikan
        if len(riwayat_konsumsi_obat) > 0:
            riwayat_konsumi_obat_pertama = riwayat_konsumsi_obat[0]

            # hitung waktu keterlambatanya
            waktu_terlambat = (riwayat_konsumi_obat_pertama.waktu_minum - waktu_konsumsi_obat_pada_jadwal).total_seconds() // 60

            riwayat.riwayat_konsumsi = riwayat_konsumi_obat_pertama
            riwayat.is_terlambat = False
            riwayat.is_terlewat = False
            riwayat.waktu_terlambat = waktu_terlambat

            # lanjutkan iterasi selanjutnya
            urutan_riwayat_jadwal += 1

            continue

        #Jika tidak ada maka cara riwayat konsumsi dari rentang waktu minum obat hingga jadwal selanjutnya
        riwayat_konsumsi_obat_terlambat = KonsumsiobatRepository.where(query=f"((id_obat=={id_obat})&(waktu_minum_between={waktu_konsumsi_obat_terlambat_pada_jadwal},{waktu_konsumsi_obat_terlambat_pada_jadwal_selanjutnya}))", db=db)

        # Jika didapatkan riwayat konsumsi obat yang terlambat
        if len(riwayat_konsumsi_obat_terlambat) > 0:
            konsumsi_obat_terlambat = riwayat_konsumsi_obat_terlambat[0]

            # hitung waktu keterlambatanya
            menit_waktu_terlambat = (konsumsi_obat_terlambat.waktu_minum - waktu_konsumsi_obat_pada_jadwal).total_seconds() // 60

            riwayat.riwayat_konsumsi = konsumsi_obat_terlambat
            riwayat.is_terlambat = True
            riwayat.is_terlewat = True
            riwayat.waktu_terlambat = menit_waktu_terlambat

            urutan_riwayat_jadwal += 1

            continue

        riwayat.riwayat_konsumsi = None
        riwayat.is_terlambat = True
        riwayat.is_terlewat = False
        riwayat.waktu_terlambat = None

        urutan_riwayat_jadwal += 1

        continue

    return riwayatjadwal

@router.get("/{riwayatjadwal_id:int}", response_model=RiwayatjadwalResponseWithKonsumsiObat)
def get_riwayatjadwal(
    riwayatjadwal_id: int,
    db: Session = Depends(get_db)
):
    riwayat_repo = RiwayatjadwalRepository.get_by_id(db, riwayatjadwal_id)
    
    riwayat = RiwayatjadwalResponseWithKonsumsiObat(
        id=riwayat_repo.id,
        id_jadwal=riwayat_repo.id_jadwal,
        waktu_riwayat=riwayat_repo.waktu_riwayat,
        created_at=riwayat_repo.created_at,
        updated_at=riwayat_repo.updated_at
    )

    id_obat = riwayat_repo.jadwals.obat.id

    riwayat.id_obat = id_obat

    # buat variabel riwayat 
    try:
        riwayat_selanjutnya = RiwayatjadwalRepository.get_by_id(db, riwayatjadwal_id + 1)
    except Exception as e:
        riwayat_selanjutnya = riwayat
        print(e)

    # buat variabel waktu konsumsi obat pada jadwal yang di ambil dari riwayat
    waktu_konsumsi_obat_pada_jadwal = riwayat.waktu_riwayat
    waktu_konsumsi_obat_pada_jadwal_selanjutnya = riwayat_selanjutnya.waktu_riwayat

    # tentukan tenggat terlambat waktu konsumsi obat berdasarkan jadwal
    waktu_konsumsi_obat_terlambat_pada_jadwal = waktu_konsumsi_obat_pada_jadwal + timedelta(minutes=45)
    waktu_konsumsi_obat_terlambat_pada_jadwal_selanjutnya = waktu_konsumsi_obat_pada_jadwal_selanjutnya + timedelta(minutes=45)

    # Lalu cari riwayat konsumsi obat pada rentang waktu_konsumsi_obat_pada_jadwal hingga waktu_konsumsi_obat_terlambat_pada_jadwal
    riwayat_konsumsi_obat = KonsumsiobatRepository.where(query=f"((id_obat=={id_obat})&(waktu_minum_between={waktu_konsumsi_obat_pada_jadwal},{waktu_konsumsi_obat_terlambat_pada_jadwal}))", db=db)

    # Jika ada maka berikan
    if len(riwayat_konsumsi_obat) > 0:
        riwayat_konsumi_obat_pertama = riwayat_konsumsi_obat[0]

        # hitung waktu keterlambatanya
        waktu_terlambat = (riwayat_konsumi_obat_pertama.waktu_minum - waktu_konsumsi_obat_pada_jadwal).total_seconds() // 60

        riwayat.riwayat_konsumsi = riwayat_konsumi_obat_pertama
        riwayat.is_terlambat = False
        riwayat.is_terlewat = False
        riwayat.waktu_terlambat = waktu_terlambat

    #Jika tidak ada maka cara riwayat konsumsi dari rentang waktu minum obat hingga jadwal selanjutnya
    riwayat_konsumsi_obat_terlambat = KonsumsiobatRepository.where(query=f"((id_obat=={id_obat})&(waktu_minum_between={waktu_konsumsi_obat_terlambat_pada_jadwal},{waktu_konsumsi_obat_terlambat_pada_jadwal_selanjutnya}))", db=db)

    # Jika didapatkan riwayat konsumsi obat yang terlambat
    if len(riwayat_konsumsi_obat_terlambat) > 0:
        konsumsi_obat_terlambat = riwayat_konsumsi_obat_terlambat[0]

        # hitung waktu keterlambatanya
        menit_waktu_terlambat = (konsumsi_obat_terlambat.waktu_minum - waktu_konsumsi_obat_pada_jadwal).total_seconds() // 60

        riwayat.riwayat_konsumsi = konsumsi_obat_terlambat
        riwayat.is_terlambat = True
        riwayat.is_terlewat = True
        riwayat.waktu_terlambat = menit_waktu_terlambat

    riwayat.riwayat_konsumsi = None
    riwayat.is_terlambat = True
    riwayat.is_terlewat = True
    riwayat.waktu_terlambat = None

    return riwayat

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