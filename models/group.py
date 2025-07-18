from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    sites: List["Site"] = Relationship(
        back_populates="group",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        }
    )
