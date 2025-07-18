from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from typing import List

from dbconfig import get_session
from models.site import Site
from models.group import Group
from schemas.site_schemas import SiteCreate, SiteRead, SiteUpdate
from utils.ping_checker import check_online_sync

from auth import authenticate

router = APIRouter(
    prefix="/sites",
    tags=["sites"],
    dependencies=[Depends(authenticate)]
)

@router.post("/", response_model=SiteRead, status_code=status.HTTP_201_CREATED)
def create_site(site: SiteCreate, session: Session = Depends(get_session)):
    group = session.get(Group, site.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")

    existing_site = session.exec(
        select(Site)
        .where(Site.name == site.name)
        .where(Site.group_id == site.group_id)
    ).first()

    if existing_site:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe um site com este nome no grupo")

    db_site = Site.from_orm(site)
    session.add(db_site)
    session.commit()
    session.refresh(db_site)

    # Retorna SiteRead com campo online — só no schema, não no modelo SQLModel
    return SiteRead(
        id=db_site.id,
        name=db_site.name,
        ip=db_site.ip,
        location=db_site.location,
        link=db_site.link,
        description=db_site.description,
        group_id=db_site.group_id,
        online=check_online_sync(db_site.ip)
    )


@router.get("/", response_model=List[SiteRead])
def read_sites(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    sites = session.exec(
        select(Site)
        .offset(skip)
        .limit(limit)
        .options(joinedload(Site.group))
    ).all()

    return [
        SiteRead(
            id=site.id,
            name=site.name,
            ip=site.ip,
            location=site.location,
            link=site.link,
            description=site.description,
            group_id=site.group_id,
            online=check_online_sync(site.ip)
        )
        for site in sites
    ]


@router.get("/{site_id}", response_model=SiteRead)
def read_site(site_id: int, session: Session = Depends(get_session)):
    site = session.exec(
        select(Site)
        .where(Site.id == site_id)
        .options(joinedload(Site.group))
    ).first()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site não encontrado")

    return SiteRead(
        id=site.id,
        name=site.name,
        ip=site.ip,
        location=site.location,
        link=site.link,
        description=site.description,
        group_id=site.group_id,
        online=check_online_sync(site.ip)
    )


@router.put("/{site_id}", response_model=SiteRead)
def update_site(site_id: int, site_data: SiteUpdate, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site não encontrado")

    if site_data.name and site_data.name != site.name:
        existing_site = session.exec(
            select(Site)
            .where(Site.name == site_data.name)
            .where(Site.group_id == site.group_id)
            .where(Site.id != site_id)
        ).first()

        if existing_site:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe um site com este nome no grupo")

    for key, value in site_data.dict(exclude_unset=True).items():
        setattr(site, key, value)

    session.add(site)
    session.commit()
    session.refresh(site)

    return SiteRead(
        id=site.id,
        name=site.name,
        ip=site.ip,
        location=site.location,
        link=site.link,
        description=site.description,
        group_id=site.group_id,
        online=check_online_sync(site.ip)
    )


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site não encontrado")

    session.delete(site)
    session.commit()
