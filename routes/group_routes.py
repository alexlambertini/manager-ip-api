from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Response
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from typing import List, Optional

from dbconfig import get_session
from models.site import Site
from models.group import Group
from schemas.group_schemas import GroupCreate, GroupRead, GroupUpdate
from schemas.site_schemas import SiteRead
from auth import authenticate

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[Depends(authenticate)]
)

@router.post("/", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(group: GroupCreate, session: Session = Depends(get_session)):
    existing_group = session.exec(select(Group).where(Group.name == group.name)).first()
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um grupo com esse nome."
        )
    
    db_group = Group.from_orm(group)
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group

@router.get("/", response_model=List[GroupRead])
def read_groups(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    
    groups = session.exec(
        select(Group)
        .options(joinedload(Group.sites))
        .offset(skip)
        .limit(limit)
    ).unique().all()

    groups_response = []
    for group in groups:
        sites_with_status = []
        for site in group.sites:
            site_data = SiteRead.from_orm(site)
            site_data.online = None  # Sem checar status aqui para não atrasar a resposta
            sites_with_status.append(site_data)
        
        group_data = GroupRead.from_orm(group)
        group_data.sites = sites_with_status
        groups_response.append(group_data)

    return groups_response

@router.get("/{group_id}", response_model=GroupRead)
def read_group(group_id: int, session: Session = Depends(get_session)):
    group = session.exec(
        select(Group)
        .where(Group.id == group_id)
        .options(joinedload(Group.sites))
    ).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo não encontrado"
        )

    sites_with_status = []
    for site in group.sites:
        site_data = SiteRead.from_orm(site)
        site_data.online = None  # Sem checar status aqui também
        sites_with_status.append(site_data)

    group_data = GroupRead.from_orm(group)
    group_data.sites = sites_with_status

    return group_data

@router.get("/{group_id}/sites", response_model=List[SiteRead])
def read_sites_by_group(
    group_id: int,
    session: Session = Depends(get_session)
):
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo não encontrado"
        )

    sites_with_status = []
    for site in group.sites:
        site_data = SiteRead.from_orm(site)
        site_data.online = None  # Também sem checar aqui
        sites_with_status.append(site_data)

    return sites_with_status

@router.put("/{group_id}", response_model=GroupRead)
def update_group(
    group_id: int,
    group_data: GroupUpdate,
    session: Session = Depends(get_session)
):
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo não encontrado"
        )

    # Verifica se o novo nome já existe
    if group_data.name != group.name:
        existing = session.exec(
            select(Group)
            .where(Group.name == group_data.name)
            .where(Group.id != group_id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um grupo com esse nome"
            )

    group.name = group_data.name

    # Gerenciamento dos sites
    existing_site_ids = {site.id for site in group.sites}
    sent_site_ids = {site.id for site in group_data.sites if site.id is not None}

    # Remove sites não enviados
    for site in list(group.sites):
        if site.id not in sent_site_ids:
            session.delete(site)

    # Atualiza ou adiciona sites
    for site_data in group_data.sites:
        if site_data.id is None:
            new_site = Site(
                name=site_data.name,
                ip=site_data.ip,
                location=site_data.location,
                group_id=group.id,
                link=site_data.link,
                description=getattr(site_data, "description", None)
            )
            session.add(new_site)
        else:
            site = session.get(Site, site_data.id)
            if site:
                site.name = site_data.name
                site.ip = site_data.ip
                site.location = site_data.location
                site.link = site_data.link
                if hasattr(site_data, "description"):
                    site.description = site_data.description

    session.commit()
    session.refresh(group)
    return group

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, session: Session = Depends(get_session)):
    try:
        group = session.exec(select(Group).where(Group.id == group_id)).first()

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo não encontrado"
            )

        print(f"Deletando grupo: {group.id}, sites vinculados: {[site.id for site in group.sites]}")

        session.delete(group)
        session.commit()

        print("Deleção confirmada no banco.")
        return None

    except Exception as e:
        print(f"Erro ao deletar grupo: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar grupo: {str(e)}"
        )
