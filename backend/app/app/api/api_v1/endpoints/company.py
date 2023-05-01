from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_companys(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve companys.
    """
    if crud.user.is_superuser(current_user):
        company = crud.company.get_multi(db=db,order_by="name")
        count = len(crud.company.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':company})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Company])
def create_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.CompanyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new company.
    """
    if crud.user.is_superuser(current_user):
        company = crud.company.create(db=db, obj_in=company_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.company.get_multi(db=db, order_by="name")


@router.put("/", response_model=List[schemas.Company])
def update_company(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    company_in: schemas.CompanyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an company.
    """
    company = crud.company.get_by_uuid(db=db, uuid=uuid)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    company = crud.company.update(db=db, db_obj=company, obj_in=company_in)
    return crud.company.get_multi(db=db, order_by="name")


@router.get("/by_uuid/", response_model=schemas.Company)
def read_company(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company by ID.
    """
    company = crud.company.get_by_uuid(db=db, uuid=uuid)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return company


@router.delete("/", response_model=List[schemas.Company])
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an company.
    """
    company = crud.company.get_by_uuid(db=db, uuid=uuid)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    company = crud.company.remove_uuid(db=db, uuid=uuid)
    return crud.company.get_multi(db=db, order_by="name")
