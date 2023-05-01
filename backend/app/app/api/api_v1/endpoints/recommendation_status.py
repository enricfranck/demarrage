from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_recommendation_statuss(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve recommendation_statuss.
    """
    if crud.user.is_superuser(current_user):
        recommendation_status = crud.recommendation_status.get_multi(db=db)
        count = len(crud.recommendation_status.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':recommendation_status})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.RecommendationStatus])
def create_recommendation_status(
    *,
    db: Session = Depends(deps.get_db),
    recommendation_status_in: schemas.RecommendationStatusCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new recommendation_status.
    """
    if crud.user.is_superuser(current_user):
        recommendation_status = crud.recommendation_status.create(db=db, obj_in=recommendation_status_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.recommendation_status.get_multi(db=db)


@router.put("/", response_model=List[schemas.RecommendationStatus])
def update_recommendation_status(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    recommendation_status_in: schemas.RecommendationStatusUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an recommendation_status.
    """
    recommendation_status = crud.recommendation_status.get_by_uuid(db=db, uuid=uuid)
    if not recommendation_status:
        raise HTTPException(status_code=404, detail="RecommendationStatus not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recommendation_status = crud.recommendation_status.update(db=db, db_obj=recommendation_status, obj_in=recommendation_status_in)
    return crud.recommendation_status.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.RecommendationStatus)
def read_recommendation_status(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recommendation_status by ID.
    """
    recommendation_status = crud.recommendation_status.get_by_uuid(db=db, uuid=uuid)
    if not recommendation_status:
        raise HTTPException(status_code=404, detail="RecommendationStatus not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return recommendation_status


@router.delete("/", response_model=List[schemas.RecommendationStatus])
def delete_recommendation_status(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an recommendation_status.
    """
    recommendation_status = crud.recommendation_status.get_by_uuid(db=db, uuid=uuid)
    if not recommendation_status:
        raise HTTPException(status_code=404, detail="RecommendationStatus not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recommendation_status = crud.recommendation_status.remove_uuid(db=db, uuid=uuid)
    return crud.recommendation_status.get_multi(db=db)
