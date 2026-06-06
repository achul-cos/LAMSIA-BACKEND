# ------------------------------------------------------------------
# user_routes.py
# ------------------------------------------------------------------
# Latar Belakang :
# Pada aplikasi API, terdapat sistem route. Jika keseluruhan API
# berfungsi untuk mengatur mengelola data User, Lansia, Kotak_Obat
# Dan ketika user ingin mengakses fitur pengelolaan data User misalnya,
# seperti ingin menambahkan data user baru; Mereka dapat mengakses route
# User dapat mengakses route User, yang ditulis dengan /User (misalnya),
# Dan di dalam route tersebut terdapat sub route seperti /User/Daftar,
# atau ada method seperti get, post, patch, update dan lainya. Variasi
# sub route dan method tersebut pada dasarnya mengarahkan user pada fitur
# yang lebih spesifik yang di definisikan pada suatu fungsi. Maka kesimpulanya,
# Route adalah grub dari route-route pada suatu objek atau class. 
#
# Definisi :
# Kode ini mendefinisikan fitur-fitur didalam route /users yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /users akan didaftarkan pada main.py
# ------------------------------------------------------------------
from fastapi import APIRouter, Depends, Request
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.create(db, user_data)
    return RepositoryResponse

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.get_all(db)
    return RepositoryResponse

@router.get("/{user_id:int}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.get_by_id(db, user_id)
    return RepositoryResponse

@router.put("/{user_id}", response_model=UserResponse)
def update_put(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.update_put(db, user_id, user_data)
    return RepositoryResponse

@router.patch("/{user_id}", response_model=UserResponse)
def update_patch(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.update_patch(db, user_id, payload)
    return RepositoryResponse

@router.delete("/{user_id}", response_model=UserResponse)
def delete(
    user_id: int,
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.delete(db, user_id)
    return RepositoryResponse

@router.post("/delete-all")
def delete_all(
    db: Session = Depends(get_db)
):
    RepositoryResponse = UserRepository.delete_all(db)
    return RepositoryResponse

@router.get("/filter", response_model=list[UserResponse])
def filter(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    RepositoryResponse = UserRepository.filter(db, **params)
    return RepositoryResponse

@router.get("/where", response_model=list[UserResponse])
def where(
    query: str,
    db: Session = Depends(get_db)
):
    return UserRepository.where(db, query)