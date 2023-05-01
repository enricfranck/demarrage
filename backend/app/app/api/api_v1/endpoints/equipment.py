from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_equipments(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve equipments.
    """
    if crud.user.is_superuser(current_user):
        equipment = crud.equipment.get_multi(db=db)
        count = len(crud.equipment.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':equipment})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Equipment])
def create_equipment(
    *,
    db: Session = Depends(deps.get_db),
    equipment_in: schemas.EquipmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new equipment.
    """
    if crud.user.is_superuser(current_user):
        equipment = crud.equipment.create(db=db, obj_in=equipment_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.equipment.get_multi(db=db)


@router.put("/", response_model=List[schemas.Equipment])
def update_equipment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    equipment_in: schemas.EquipmentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an equipment.
    """
    equipment = crud.equipment.get_by_uuid(db=db, uuid=uuid)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    equipment = crud.equipment.update(db=db, db_obj=equipment, obj_in=equipment_in)
    return crud.equipment.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Equipment)
def read_equipment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get equipment by ID.
    """
    equipment = crud.equipment.get_by_uuid(db=db, uuid=uuid)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return equipment


@router.delete("/", response_model=List[schemas.Equipment])
def delete_equipment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an equipment.
    """
    equipment = crud.equipment.get_by_uuid(db=db, uuid=uuid)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    equipment = crud.equipment.remove_uuid(db=db, uuid=uuid)
    return crud.equipment.get_multi(db=db)
