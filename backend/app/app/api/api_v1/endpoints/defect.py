from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_defects(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve defects.
    """
    if crud.user.is_superuser(current_user):
        defect = crud.defect.get_multi(db=db)
        count = len(crud.defect.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':defect})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Defect])
def create_defect(
    *,
    db: Session = Depends(deps.get_db),
    defect_in: schemas.DefectCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new defect.
    """
    if crud.user.is_superuser(current_user):
        defect = crud.defect.create(db=db, obj_in=defect_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.defect.get_multi(db=db)


@router.put("/", response_model=List[schemas.Defect])
def update_defect(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    defect_in: schemas.DefectUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an defect.
    """
    defect = crud.defect.get_by_uuid(db=db, uuid=uuid)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    defect = crud.defect.update(db=db, db_obj=defect, obj_in=defect_in)
    return crud.defect.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Defect)
def read_defect(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get defect by ID.
    """
    defect = crud.defect.get_by_uuid(db=db, uuid=uuid)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return defect


@router.delete("/", response_model=List[schemas.Defect])
def delete_defect(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an defect.
    """
    defect = crud.defect.get_by_uuid(db=db, uuid=uuid)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    defect = crud.defect.remove_uuid(db=db, uuid=uuid)
    return crud.defect.get_multi(db=db)
