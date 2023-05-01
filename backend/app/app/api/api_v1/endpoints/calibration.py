from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_calibrations(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve calibrations.
    """
    if crud.user.is_superuser(current_user):
        calibration = crud.calibration.get_multi(db=db)
        count = len(crud.calibration.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':calibration})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Calibration])
def create_calibration(
    *,
    db: Session = Depends(deps.get_db),
    calibration_in: schemas.CalibrationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new calibration.
    """
    if crud.user.is_superuser(current_user):
        calibration = crud.calibration.create(db=db, obj_in=calibration_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.calibration.get_multi(db=db)


@router.put("/", response_model=List[schemas.Calibration])
def update_calibration(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    calibration_in: schemas.CalibrationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an calibration.
    """
    calibration = crud.calibration.get_by_uuid(db=db, uuid=uuid)
    if not calibration:
        raise HTTPException(status_code=404, detail="Calibration not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    calibration = crud.calibration.update(db=db, db_obj=calibration, obj_in=calibration_in)
    return crud.calibration.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Calibration)
def read_calibration(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get calibration by ID.
    """
    calibration = crud.calibration.get_by_uuid(db=db, uuid=uuid)
    if not calibration:
        raise HTTPException(status_code=404, detail="Calibration not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return calibration


@router.delete("/", response_model=List[schemas.Calibration])
def delete_calibration(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an calibration.
    """
    calibration = crud.calibration.get_by_uuid(db=db, uuid=uuid)
    if not calibration:
        raise HTTPException(status_code=404, detail="Calibration not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    calibration = crud.calibration.remove_uuid(db=db, uuid=uuid)
    return crud.calibration.get_multi(db=db)
