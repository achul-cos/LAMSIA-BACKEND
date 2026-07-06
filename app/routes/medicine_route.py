from typing import List
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.medicine_model import Medicine
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.medicine_schema import MedicineCreate, MedicineResponse
from app.repositories.medicine_repository import MedicineRepository

router = APIRouter(
  prefix="/medicines",
  tags=['medicines']
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post('/', response_model=MedicineResponse)
def create_medicine(
  medicine_data:MedicineCreate,
  db: Session = Depends(get_db)
):
  RepositoryResponse = MedicineRepository.create(db, medicine_data)
  return RepositoryResponse

@router.get('/', response_model=List[MedicineResponse])
def get_all_medicines(db: Session = Depends(get_db)):
  medicines = db.query(Medicine).all()
  return medicines

@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
  medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

  if not medicine:
    raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
  
  try:
    db.delete(medicine)
    db.commit()
    return {"status": "success", "message": f"Obat dengan id ${medicine_id} berhasil dihapus"}
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Gagal menghapus data: {str(e)}")
