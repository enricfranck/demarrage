from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_teams(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve teams.
    """
    if crud.user.is_superuser(current_user):
        team = crud.team.get_multi(db=db,order_by="name")
        count = len(crud.team.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':team})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Team])
def create_team(
    *,
    db: Session = Depends(deps.get_db),
    team_in: schemas.TeamCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new team.
    """
    if crud.user.is_superuser(current_user):
        team = crud.team.create(db=db, obj_in=team_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.team.get_multi(db=db, order_by="name")


@router.put("/", response_model=List[schemas.Team])
def update_team(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    team_in: schemas.TeamUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an team.
    """
    team = crud.team.get_by_uuid(db=db, uuid=uuid)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    team = crud.team.update(db=db, db_obj=team, obj_in=team_in)
    return crud.team.get_multi(db=db, order_by="name")


@router.get("/by_uuid/", response_model=schemas.Team)
def read_team(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get team by ID.
    """
    team = crud.team.get_by_uuid(db=db, uuid=uuid)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return team


@router.delete("/", response_model=List[schemas.Team])
def delete_team(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an team.
    """
    team = crud.team.get_by_uuid(db=db, uuid=uuid)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    team = crud.team.remove_uuid(db=db, uuid=uuid)
    return crud.team.get_multi(db=db, order_by="name")
