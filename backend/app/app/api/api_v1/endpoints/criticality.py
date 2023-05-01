from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_criticalitys(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve criticalitys.
    """
    if crud.user.is_superuser(current_user):
        criticality = crud.criticality.get_multi(db=db)
        count = len(crud.criticality.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':criticality})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Criticality])
def create_criticality(
    *,
    db: Session = Depends(deps.get_db),
    criticality_in: schemas.CriticalityCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new criticality.
    """
    if crud.user.is_superuser(current_user):
        criticality = crud.criticality.create(db=db, obj_in=criticality_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.criticality.get_multi(db=db)


@router.put("/", response_model=List[schemas.Criticality])
def update_criticality(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    criticality_in: schemas.CriticalityUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an criticality.
    """
    criticality = crud.criticality.get_by_uuid(db=db, uuid=uuid)
    if not criticality:
        raise HTTPException(status_code=404, detail="Criticality not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    criticality = crud.criticality.update(db=db, db_obj=criticality, obj_in=criticality_in)
    return crud.criticality.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Criticality)
def read_criticality(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get criticality by ID.
    """
    criticality = crud.criticality.get_by_uuid(db=db, uuid=uuid)
    if not criticality:
        raise HTTPException(status_code=404, detail="Criticality not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return criticality


@router.delete("/", response_model=List[schemas.Criticality])
def delete_criticality(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an criticality.
    """
    criticality = crud.criticality.get_by_uuid(db=db, uuid=uuid)
    if not criticality:
        raise HTTPException(status_code=404, detail="Criticality not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    criticality = crud.criticality.remove_uuid(db=db, uuid=uuid)
    return crud.criticality.get_multi(db=db)
