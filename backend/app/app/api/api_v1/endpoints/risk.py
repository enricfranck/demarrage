from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_risks(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve risks.
    """
    if crud.user.is_superuser(current_user):
        risk = crud.risk.get_multi(db=db,order_by="value")
        count = len(crud.risk.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':risk})
    else:
        raise HTTPException(risk_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Risk])
def create_risk(
    *,
    db: Session = Depends(deps.get_db),
    risk_in: schemas.RiskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new risk.
    """
    if crud.user.is_superuser(current_user):
        risk = crud.risk.create(db=db, obj_in=risk_in)
    else:
        raise HTTPException(risk_code=400, detail="Not enough permissions")
    return crud.risk.get_multi(db=db, order_by="value")


@router.put("/", response_model=List[schemas.Risk])
def update_risk(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    risk_in: schemas.RiskUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an risk.
    """
    risk = crud.risk.get_by_uuid(db=db, uuid=uuid)
    if not risk:
        raise HTTPException(risk_code=404, detail="Risk not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(risk_code=400, detail="Not enough permissions")
    risk = crud.risk.update(db=db, db_obj=risk, obj_in=risk_in)
    return crud.risk.get_multi(db=db, order_by="value")


@router.get("/by_uuid/", response_model=schemas.Risk)
def read_risk(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get risk by ID.
    """
    risk = crud.risk.get_by_uuid(db=db, uuid=uuid)
    if not risk:
        raise HTTPException(risk_code=404, detail="Risk not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(risk_code=400, detail="Not enough permissions")
    return risk


@router.delete("/", response_model=List[schemas.Risk])
def delete_risk(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an risk.
    """
    risk = crud.risk.get_by_uuid(db=db, uuid=uuid)
    if not risk:
        raise HTTPException(risk_code=404, detail="Risk not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(risk_code=400, detail="Not enough permissions")
    risk = crud.risk.remove_uuid(db=db, uuid=uuid)
    return crud.risk.get_multi(db=db, order_by="value")
