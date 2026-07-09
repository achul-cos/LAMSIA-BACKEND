# ------------------------------------------------------------------
# dashboard_route.py.py
# ------------------------------------------------------------------
# Kode ini mendefinisikan fitur-fitur didalam route /dashboards yang didefinisikan
# dengan fungsi-fungsi yang diintegrasikan dengan variasi sub-route dan methodnya
# yang selanjutnya route /dashboards akan didaftarkan pada main.py
# ------------------------------------------------------------------
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request

from app.schemas.dashboard_schema import DashboardResponse
from app.repositories.dashboard_repository import DashboardRepository
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/dashboards",
    tags=["Dashboards"]
)

# @router.post("/", response_model=DashboardResponse)
# def create_dashboard(
#     dashboard_data: DashboardCreate,
#     db: Session = Depends(get_db)
# ):
#     RepositoryResponse = DashboardRepository.create(db, dashboard_data)
#     return RepositoryResponse

@router.get("/", response_model=DashboardResponse)
def get_dashboards(
    db: Session = Depends(get_db)
):
    RepositoryResponse = DashboardRepository.get_dashboard(db)
    return RepositoryResponse

# @router.get("/{dashboard_id:int}", response_model=DashboardResponse)
# def get_dashboard(
#     dashboard_id: int,
#     db: Session = Depends(get_db)
# ):
#     RepositoryResponse = DashboardRepository.get_by_id(db, dashboard_id)
#     return RepositoryResponse

# @router.put("/{dashboard_id}", response_model=DashboardResponse)
# def update_put(
#     dashboard_id: int,
#     dashboard_data: DashboardUpdate,
#     db: Session = Depends(get_db)
# ):
#     RepositoryResponse = DashboardRepository.update_put(db, dashboard_id, dashboard_data)
#     return RepositoryResponse

# @router.patch("/{dashboard_id}", response_model=DashboardResponse)
# def update_patch(
#     dashboard_id: int,
#     payload: dict,
#     db: Session = Depends(get_db)
# ):
#     RepositoryResponse = DashboardRepository.update_patch(db, dashboard_id, payload)
#     return RepositoryResponse

# @router.delete("/{dashboard_id}", response_model=DashboardResponse)
# def delete(
#     dashboard_id: int,
#     db: Session = Depends(get_db)
# ):
#     RepositoryResponse = DashboardRepository.delete(db, dashboard_id)
#     return RepositoryResponse

# @router.post("/delete-all")
# def delete_all(
#     db: Session = Depends(get_db)
# ):
#     RepositoryResponse = DashboardRepository.delete_all(db)
#     return RepositoryResponse

# @router.get("/filter", response_model=list[DashboardResponse])
# def filter(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     params = dict(request.query_params)
#     RepositoryResponse = DashboardRepository.filter(db, **params)
#     return RepositoryResponse

# @router.get("/where", response_model=list[DashboardResponse])
# def where(
#     query: str,
#     db: Session = Depends(get_db)
# ):
#     return DashboardRepository.where(db, query)