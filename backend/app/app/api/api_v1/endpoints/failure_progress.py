from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_failure_progresss(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve failure_progresss.
    """
    if crud.user.is_superuser(current_user):
        failure_progress = crud.failure_progress.get_multi(db=db)
        count = len(crud.failure_progress.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':failure_progress})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.FailureProgress])
def create_failure_progress(
    *,
    db: Session = Depends(deps.get_db),
    failure_progress_in: schemas.FailureProgressCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new failure_progress.
    """
    if crud.user.is_superuser(current_user):
        failure_progress = crud.failure_progress.create(db=db, obj_in=failure_progress_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.failure_progress.get_multi(db=db)


@router.put("/", response_model=List[schemas.FailureProgress])
def update_failure_progress(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    failure_progress_in: schemas.FailureProgressUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an failure_progress.
    """
    failure_progress = crud.failure_progress.get_by_uuid(db=db, uuid=uuid)
    if not failure_progress:
        raise HTTPException(status_code=404, detail="FailureProgress not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    failure_progress = crud.failure_progress.update(db=db, db_obj=failure_progress, obj_in=failure_progress_in)
    return crud.failure_progress.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.FailureProgress)
def read_failure_progress(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get failure_progress by ID.
    """
    failure_progress = crud.failure_progress.get_by_uuid(db=db, uuid=uuid)
    if not failure_progress:
        raise HTTPException(status_code=404, detail="FailureProgress not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return failure_progress


@router.delete("/", response_model=List[schemas.FailureProgress])
def delete_failure_progress(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an failure_progress.
    """
    failure_progress = crud.failure_progress.get_by_uuid(db=db, uuid=uuid)
    if not failure_progress:
        raise HTTPException(status_code=404, detail="FailureProgress not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    failure_progress = crud.failure_progress.remove_uuid(db=db, uuid=uuid)
    return crud.failure_progress.get_multi(db=db)
