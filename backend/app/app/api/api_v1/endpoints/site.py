from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_sites(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve sites.
    """
    if crud.user.is_superuser(current_user):
        site = crud.site.get_multi(db=db,order_by="name")
        count = len(crud.site.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':site})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Site])
def create_site(
    *,
    db: Session = Depends(deps.get_db),
    site_in: schemas.SiteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new site.
    """
    if crud.user.is_superuser(current_user):
        site = crud.site.create(db=db, obj_in=site_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.site.get_multi(db=db, order_by="name")


@router.put("/", response_model=List[schemas.Site])
def update_site(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    site_in: schemas.SiteUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an site.
    """
    site = crud.site.get_by_uuid(db=db, uuid=uuid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    site = crud.site.update(db=db, db_obj=site, obj_in=site_in)
    return crud.site.get_multi(db=db, order_by="name")


@router.get("/by_uuid/", response_model=schemas.Site)
def read_site(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get site by ID.
    """
    site = crud.site.get_by_uuid(db=db, uuid=uuid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return site


@router.delete("/", response_model=List[schemas.Site])
def delete_site(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an site.
    """
    site = crud.site.get_by_uuid(db=db, uuid=uuid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    site = crud.site.remove_uuid(db=db, uuid=uuid)
    return crud.site.get_multi(db=db, order_by="name")
