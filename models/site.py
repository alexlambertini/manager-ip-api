from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
from typing import Optional

class Site(SQLModel, table=True):
    __tablename__ = "sites"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: str
    location: str

    group_id: int = Field(
        sa_column=Column(
            ForeignKey("groups.id", ondelete="CASCADE"),
            nullable=False
        )
    )

    link: Optional[str] = Field(default=None, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)

    group: Optional["Group"] = Relationship(back_populates="sites")
