from pydantic import BaseModel

class MedicineCreate(BaseModel):
  name: str
  dosage: int
  form: str
  times: int
  quantity: int
  kompartemen: int
  repeat: str

class MedicineResponse(MedicineCreate):
  id: int

  class Config:
    from_attributes = True
