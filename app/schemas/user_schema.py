from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    telephone: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    telephone: str

    class Config:
        from_attribute = True