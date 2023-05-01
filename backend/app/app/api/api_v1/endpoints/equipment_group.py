from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_equipment_groups(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve equipment_groups.
    """
    if crud.user.is_superuser(current_user):
        equipment_group = crud.equipment_group.get_multi(db=db)
        count = len(crud.equipment_group.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':equipment_group})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.EquipmentGroup])
def create_equipment_group(
    *,
    db: Session = Depends(deps.get_db),
    equipment_group_in: schemas.EquipmentGroupCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new equipment_group.
    """
    if crud.user.is_superuser(current_user):
        equipment_group = crud.equipment_group.create(db=db, obj_in=equipment_group_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.equipment_group.get_multi(db=db)


@router.put("/", response_model=List[schemas.EquipmentGroup])
def update_equipment_group(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    equipment_group_in: schemas.EquipmentGroupUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an equipment_group.
    """
    equipment_group = crud.equipment_group.get_by_uuid(db=db, uuid=uuid)
    if not equipment_group:
        raise HTTPException(status_code=404, detail="EquipmentGroup not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    equipment_group = crud.equipment_group.update(db=db, db_obj=equipment_group, obj_in=equipment_group_in)
    return crud.equipment_group.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.EquipmentGroup)
def read_equipment_group(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get equipment_group by ID.
    """
    equipment_group = crud.equipment_group.get_by_uuid(db=db, uuid=uuid)
    if not equipment_group:
        raise HTTPException(status_code=404, detail="EquipmentGroup not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return equipment_group


@router.delete("/", response_model=List[schemas.EquipmentGroup])
def delete_equipment_group(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an equipment_group.
    """
    equipment_group = crud.equipment_group.get_by_uuid(db=db, uuid=uuid)
    if not equipment_group:
        raise HTTPException(status_code=404, detail="EquipmentGroup not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    equipment_group = crud.equipment_group.remove_uuid(db=db, uuid=uuid)
    return crud.equipment_group.get_multi(db=db)
