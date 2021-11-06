from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Parcours])
def read_parcours(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve paarcours.
    """
    if crud.user.is_superuser(current_user):
        parcours = crud.parcours.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return parcours


@router.post("/", response_model=schemas.Parcours)
def create_parcours(
    *,
    db: Session = Depends(deps.get_db),
    paarcours_in: schemas.ParcoursCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new parcours.
    """
    if crud.user.is_superuser(current_user):
        parcours = crud.parcours.create(db=db, obj_in=paarcours_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return parcours


@router.put("/{id}", response_model=schemas.Parcours)
def update_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    parcours_in: schemas.ParcoursUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an parcours.
    """
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid)
    if not parcours:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    parcours = crud.mention.update(db=db, db_obj=parcours, obj_in=parcours_in)
    return parcours


@router.get("/{uuid}", response_model=schemas.Parcours)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get parcours by ID.
    """
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid)
    if not parcours:
        raise HTTPException(status_code=404, detail="Parcours not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return parcours


@router.delete("/{uuid}", response_model=schemas.Parcours)
def delete_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an parcours.
    """
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid)
    if not parcours:
        raise HTTPException(status_code=404, detail="Parcours not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    parcours = crud.parcours.remove_uuid(db=db, uuid=uuid)
    return parcours
