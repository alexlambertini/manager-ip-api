from pydantic import BaseModel, Field
from typing import  Optional
from datetime import datetime
    

class SiteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Meu Site")
    ip: str = Field(..., pattern=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', example="192.168.1.1")
    location: str = Field(..., min_length=2, max_length=50, example="São Paulo")
    link: Optional[str] = Field(None, max_length=255, example="https://meusite.com")
    description: Optional[str] = Field(None, max_length=500, example="Site principal")
    group_id: int = Field(..., gt=0, example=1)

class SiteCreate(SiteBase):
    pass

class SiteRead(SiteBase):
    id: int
    online: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SiteUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Meu Site Atualizado")
    ip: Optional[str] = Field(None, pattern=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', example="192.168.1.2")
    location: Optional[str] = Field(None, min_length=2, max_length=50, example="Rio de Janeiro")
    link: Optional[str] = Field(None, max_length=255, example="https://meusite-novo.com")
    description: Optional[str] = Field(None, max_length=500, example="Site principal atualizado")


