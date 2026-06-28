from pydantic import BaseModel

class MedicineCreate(BaseModel):
  name: str
  dosage: int
  form: str
  times: int
  repeat: str

class MedicineResponse(MedicineCreate):
  id: int

  class Config:
    from_attributes = True
