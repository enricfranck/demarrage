from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_assessments(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve assessments.
    """
    if crud.user.is_superuser(current_user):
        assessment = crud.assessment.get_multi(db=db,order_by="name")
        count = len(crud.assessment.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':assessment})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Assessment])
def create_assessment(
    *,
    db: Session = Depends(deps.get_db),
    assessment_in: schemas.AssessmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new assessment.
    """
    if crud.user.is_superuser(current_user):
        assessment = crud.assessment.create(db=db, obj_in=assessment_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.assessment.get_multi(db=db, order_by="name")


@router.put("/", response_model=List[schemas.Assessment])
def update_assessment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    assessment_in: schemas.AssessmentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an assessment.
    """
    assessment = crud.assessment.get_by_uuid(db=db, uuid=uuid)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    assessment = crud.assessment.update(db=db, db_obj=assessment, obj_in=assessment_in)
    return crud.assessment.get_multi(db=db, order_by="name")


@router.get("/by_uuid/", response_model=schemas.Assessment)
def read_assessment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get assessment by ID.
    """
    assessment = crud.assessment.get_by_uuid(db=db, uuid=uuid)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return assessment

@router.get("/by_equipment/", response_model=schemas.Assessment)
def read_assessment_by_equipment(
    *,
    db: Session = Depends(deps.get_db),
    equipment_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get assessment by ID.
    """
    assessment = crud.assessment.get_by_equipment_id(db=db, equipment_id=equipment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return assessment

@router.delete("/", response_model=List[schemas.Assessment])
def delete_assessment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an assessment.
    """
    assessment = crud.assessment.get_by_uuid(db=db, uuid=uuid)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    assessment = crud.assessment.remove_uuid(db=db, uuid=uuid)
    return crud.assessment.get_multi(db=db, order_by="name")
