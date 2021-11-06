from os import SEEK_HOLE
from typing import Any, List
import uuid

from sqlalchemy.sql import schema

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{schema}", response_model=List[Any])
def read_etudiant_ancienne(*,
    db: Session = Depends(deps.get_db),
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve etudiant ancienne.
    """
    if crud.user.is_superuser(current_user):
        etudiant = crud.ancien_etudiant.get_all(schema=schema)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return etudiant


@router.post("/{schema}", response_model=List[Any])
def create_etudiant_ancien(
    *,
    db: Session = Depends(deps.get_db),
    etudiant_in: schemas.EtudiantAncienCreate,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new etudiant.
    """
    etudiant_in.uuid = uuid.uuid4()
    etudiant = crud.ancien_etudiant.create_etudiant(schema=schema, obj_in=etudiant_in)
    return etudiant


@router.put("/update_etudiant/{num_carte}", response_model=List[Any])
def update_etudiant(
    *,
    num_carte: str,
    schema: str,
    etudiant_in: schemas.EtudiantAncienUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    """
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    etudiant = crud.ancien_etudiant.update_etudiant(schema=schema,num_carte=num_carte, obj_in=etudiant_in)
    return etudiant


@router.get("/by_num/{schema}", response_model=Any)
def read_etudiant_by_num_carte(
    *,
    schema: str,
    num_carte: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by num carte.
    """
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return etudiant


@router.delete("/{num_carte}", response_model=List[Any])
def delete_etudiant(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an etudiant.
    """
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    etudiant = crud.ancien_etudiant.delete_etudiant(schema=schema, num_carte=num_carte)
    return etudiant
