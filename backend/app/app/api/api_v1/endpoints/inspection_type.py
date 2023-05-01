from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_inspection_types(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve inspection_types.
    """
    if crud.user.is_superuser(current_user):
        inspection_type = crud.inspection_type.get_multi(db=db,order_by="title")
        count = len(crud.inspection_type.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':inspection_type})
    else:
        raise HTTPException(inspection_type_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.InspectionType])
def create_inspection_type(
    *,
    db: Session = Depends(deps.get_db),
    inspection_type_in: schemas.InspectionTypeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new inspection_type.
    """
    if crud.user.is_superuser(current_user):
        inspection_type = crud.inspection_type.create(db=db, obj_in=inspection_type_in)
    else:
        raise HTTPException(inspection_type_code=400, detail="Not enough permissions")
    return crud.inspection_type.get_multi(db=db, order_by="title")


@router.put("/", response_model=List[schemas.InspectionType])
def update_inspection_type(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    inspection_type_in: schemas.InspectionTypeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an inspection_type.
    """
    inspection_type = crud.inspection_type.get_by_uuid(db=db, uuid=uuid)
    if not inspection_type:
        raise HTTPException(inspection_type_code=404, detail="InspectionType not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(inspection_type_code=400, detail="Not enough permissions")
    inspection_type = crud.inspection_type.update(db=db, db_obj=inspection_type, obj_in=inspection_type_in)
    return crud.inspection_type.get_multi(db=db, order_by="title")


@router.get("/by_uuid/", response_model=schemas.InspectionType)
def read_inspection_type(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inspection_type by ID.
    """
    inspection_type = crud.inspection_type.get_by_uuid(db=db, uuid=uuid)
    if not inspection_type:
        raise HTTPException(inspection_type_code=404, detail="InspectionType not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(inspection_type_code=400, detail="Not enough permissions")
    return inspection_type


@router.delete("/", response_model=List[schemas.InspectionType])
def delete_inspection_type(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an inspection_type.
    """
    inspection_type = crud.inspection_type.get_by_uuid(db=db, uuid=uuid)
    if not inspection_type:
        raise HTTPException(inspection_type_code=404, detail="InspectionType not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(inspection_type_code=400, detail="Not enough permissions")
    inspection_type = crud.inspection_type.remove_uuid(db=db, uuid=uuid)
    return crud.inspection_type.get_multi(db=db, order_by="title")
