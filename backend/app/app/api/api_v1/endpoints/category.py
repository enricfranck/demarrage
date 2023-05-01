from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_categorys(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve categorys.
    """
    if crud.user.is_superuser(current_user):
        category = crud.category.get_multi(db=db,order_by="title")
        count = len(crud.category.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':category})
    else:
        raise HTTPException(category_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Category])
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new category.
    """
    if crud.user.is_superuser(current_user):
        category = crud.category.create(db=db, obj_in=category_in)
    else:
        raise HTTPException(category_code=400, detail="Not enough permissions")
    return crud.category.get_multi(db=db, order_by="title")


@router.put("/", response_model=List[schemas.Category])
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an category.
    """
    category = crud.category.get_by_uuid(db=db, uuid=uuid)
    if not category:
        raise HTTPException(category_code=404, detail="Category not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(category_code=400, detail="Not enough permissions")
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return crud.category.get_multi(db=db, order_by="title")


@router.get("/by_uuid/", response_model=schemas.Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get category by ID.
    """
    category = crud.category.get_by_uuid(db=db, uuid=uuid)
    if not category:
        raise HTTPException(category_code=404, detail="Category not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(category_code=400, detail="Not enough permissions")
    return category


@router.delete("/", response_model=List[schemas.Category])
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an category.
    """
    category = crud.category.get_by_uuid(db=db, uuid=uuid)
    if not category:
        raise HTTPException(category_code=404, detail="Category not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(category_code=400, detail="Not enough permissions")
    category = crud.category.remove_uuid(db=db, uuid=uuid)
    return crud.category.get_multi(db=db, order_by="title")
