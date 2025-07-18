from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .site_schemas import SiteRead, SiteUpdate

class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Grupo Principal")

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: int
    sites: List[SiteRead] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Grupo Principal Atualizado")
    sites: Optional[List[SiteUpdate]] = [] 
