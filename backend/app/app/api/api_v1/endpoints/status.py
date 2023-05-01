from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_statuss(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve statuss.
    """
    if crud.user.is_superuser(current_user):
        status = crud.status.get_multi(db=db,order_by="title")
        count = len(crud.status.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':status})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Status])
def create_status(
    *,
    db: Session = Depends(deps.get_db),
    status_in: schemas.StatusCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new status.
    """
    if crud.user.is_superuser(current_user):
        status = crud.status.create(db=db, obj_in=status_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.status.get_multi(db=db, order_by="title")


@router.put("/", response_model=List[schemas.Status])
def update_status(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    status_in: schemas.StatusUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an status.
    """
    status = crud.status.get_by_uuid(db=db, uuid=uuid)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    status = crud.status.update(db=db, db_obj=status, obj_in=status_in)
    return crud.status.get_multi(db=db, order_by="title")


@router.get("/by_uuid/", response_model=schemas.Status)
def read_status(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get status by ID.
    """
    status = crud.status.get_by_uuid(db=db, uuid=uuid)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status


@router.delete("/", response_model=List[schemas.Status])
def delete_status(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an status.
    """
    status = crud.status.get_by_uuid(db=db, uuid=uuid)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    status = crud.status.remove_uuid(db=db, uuid=uuid)
    return crud.status.get_multi(db=db, order_by="title")
