from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_inspection_conditions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve inspection_conditions.
    """
    if crud.user.is_superuser(current_user):
        inspection_condition = crud.inspection_condition.get_multi(db=db,order_by="title")
        count = len(crud.inspection_condition.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':inspection_condition})
    else:
        raise HTTPException(inspection_condition_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.InspectionCondition])
def create_inspection_condition(
    *,
    db: Session = Depends(deps.get_db),
    inspection_condition_in: schemas.InspectionConditionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new inspection_condition.
    """
    if crud.user.is_superuser(current_user):
        inspection_condition = crud.inspection_condition.create(db=db, obj_in=inspection_condition_in)
    else:
        raise HTTPException(inspection_condition_code=400, detail="Not enough permissions")
    return crud.inspection_condition.get_multi(db=db, order_by="title")


@router.put("/", response_model=List[schemas.InspectionCondition])
def update_inspection_condition(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    inspection_condition_in: schemas.InspectionConditionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an inspection_condition.
    """
    inspection_condition = crud.inspection_condition.get_by_uuid(db=db, uuid=uuid)
    if not inspection_condition:
        raise HTTPException(inspection_condition_code=404, detail="InspectionCondition not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(inspection_condition_code=400, detail="Not enough permissions")
    inspection_condition = crud.inspection_condition.update(db=db, db_obj=inspection_condition, obj_in=inspection_condition_in)
    return crud.inspection_condition.get_multi(db=db, order_by="title")


@router.get("/by_uuid/", response_model=schemas.InspectionCondition)
def read_inspection_condition(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inspection_condition by ID.
    """
    inspection_condition = crud.inspection_condition.get_by_uuid(db=db, uuid=uuid)
    if not inspection_condition:
        raise HTTPException(inspection_condition_code=404, detail="InspectionCondition not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(inspection_condition_code=400, detail="Not enough permissions")
    return inspection_condition


@router.delete("/", response_model=List[schemas.InspectionCondition])
def delete_inspection_condition(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an inspection_condition.
    """
    inspection_condition = crud.inspection_condition.get_by_uuid(db=db, uuid=uuid)
    if not inspection_condition:
        raise HTTPException(inspection_condition_code=404, detail="InspectionCondition not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(inspection_condition_code=400, detail="Not enough permissions")
    inspection_condition = crud.inspection_condition.remove_uuid(db=db, uuid=uuid)
    return crud.inspection_condition.get_multi(db=db, order_by="title")
