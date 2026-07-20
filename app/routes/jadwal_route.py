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

from app.schemas.jadwal_schema import JadwalCreate, JadwalResponse, JadwalUpdate, RiwayatJadwalResponseAtJadwal
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

        riwayatjadwal : list[RiwayatJadwalResponseAtJadwal] = jadwal.riwayatjadwals
        id_obat = jadwal.id_obat
        
        urutan_riwayat_jadwal = 0

        # Iterasi versi kedua
        while urutan_riwayat_jadwal < len(riwayatjadwal):
            
            # buat variabel riwayat berdasarkan urutan iterasinya
            riwayat : RiwayatJadwalResponseAtJadwal = riwayatjadwal[urutan_riwayat_jadwal]

            # buat variabel riwayat 
            if urutan_riwayat_jadwal + 1 < len(riwayatjadwal):
                riwayat_selanjutnya : RiwayatJadwalResponseAtJadwal = riwayatjadwal[urutan_riwayat_jadwal + 1]
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

    return jadwals

@router.get("/{jadwal_id:int}", response_model=JadwalResponse)
def get_jadwal(
    jadwal_id: int,
    db: Session = Depends(get_db)
):
    jadwal = JadwalRepository.get_by_id(db, jadwal_id)

    riwayatjadwal : list[RiwayatJadwalResponseAtJadwal] = jadwal.riwayatjadwals
    id_obat = jadwal.id_obat
    
    urutan_riwayat_jadwal = 0

    # Iterasi versi kedua
    while urutan_riwayat_jadwal < len(riwayatjadwal):
        
        # buat variabel riwayat berdasarkan urutan iterasinya
        riwayat : RiwayatJadwalResponseAtJadwal = riwayatjadwal[urutan_riwayat_jadwal]

        # buat variabel riwayat 
        if urutan_riwayat_jadwal + 1 < len(riwayatjadwal):
            riwayat_selanjutnya : RiwayatJadwalResponseAtJadwal = riwayatjadwal[urutan_riwayat_jadwal + 1]
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

    return jadwal

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
    jadwals = JadwalRepository.where(db, query)

    for jadwal in jadwals:

        riwayatjadwal : list[RiwayatJadwalResponseAtJadwal] = jadwal.riwayatjadwals
        id_obat = jadwal.id_obat
        
        urutan_riwayat_jadwal = 0

        # Iterasi versi kedua
        while urutan_riwayat_jadwal < len(riwayatjadwal):
            
            # buat variabel riwayat berdasarkan urutan iterasinya
            riwayat : RiwayatJadwalResponseAtJadwal = riwayatjadwal[urutan_riwayat_jadwal]

            # buat variabel riwayat 
            if urutan_riwayat_jadwal + 1 < len(riwayatjadwal):
                riwayat_selanjutnya : RiwayatJadwalResponseAtJadwal = riwayatjadwal[urutan_riwayat_jadwal + 1]
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

    return jadwals