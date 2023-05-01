from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_records(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve records.
    """
    if crud.user.is_superuser(current_user):
        record = crud.record.get_multi(db=db)
        count = len(crud.record.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':record})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Record])
def create_record(
    *,
    db: Session = Depends(deps.get_db),
    record_in: schemas.RecordCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new record.
    """
    if crud.user.is_superuser(current_user):
        record = crud.record.create(db=db, obj_in=record_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.record.get_multi(db=db)


@router.put("/", response_model=List[schemas.Record])
def update_record(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    record_in: schemas.RecordUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an record.
    """
    record = crud.record.get_by_uuid(db=db, uuid=uuid)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    record = crud.record.update(db=db, db_obj=record, obj_in=record_in)
    return crud.record.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Record)
def read_record(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get record by ID.
    """
    record = crud.record.get_by_uuid(db=db, uuid=uuid)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return record


@router.delete("/", response_model=List[schemas.Record])
def delete_record(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an record.
    """
    record = crud.record.get_by_uuid(db=db, uuid=uuid)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    record = crud.record.remove_uuid(db=db, uuid=uuid)
    return crud.record.get_multi(db=db)
