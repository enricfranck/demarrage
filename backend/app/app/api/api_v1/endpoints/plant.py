from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_plants(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve plants.
    """
    if crud.user.is_superuser(current_user):
        plant = crud.plant.get_multi(db=db)
        count = len(crud.plant.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':plant})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Plant])
def create_plant(
    *,
    db: Session = Depends(deps.get_db),
    plant_in: schemas.PlantCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new plant.
    """
    if crud.user.is_superuser(current_user):
        plant = crud.plant.create(db=db, obj_in=plant_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.plant.get_multi(db=db)


@router.put("/", response_model=List[schemas.Plant])
def update_plant(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    plant_in: schemas.PlantUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an plant.
    """
    plant = crud.plant.get_by_uuid(db=db, uuid=uuid)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    plant = crud.plant.update(db=db, db_obj=plant, obj_in=plant_in)
    return crud.plant.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Plant)
def read_plant(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get plant by ID.
    """
    plant = crud.plant.get_by_uuid(db=db, uuid=uuid)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return plant


@router.delete("/", response_model=List[schemas.Plant])
def delete_plant(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an plant.
    """
    plant = crud.plant.get_by_uuid(db=db, uuid=uuid)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    plant = crud.plant.remove_uuid(db=db, uuid=uuid)
    return crud.plant.get_multi(db=db)
