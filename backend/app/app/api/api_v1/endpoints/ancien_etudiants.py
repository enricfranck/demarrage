from os import SEEK_HOLE
from typing import Any, List
import uuid, json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils import UUIDEncoder
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_ancienne(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve etudiant ancienne.
    """
    etudiant = crud.ancien_etudiant.get_all(schema=schema)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.post("/{schema}", response_model=List[schemas.EtudiantAncien])
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
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=etudiant_in.num_carte)
    if etudiant:
        raise HTTPException(status_code=404, detail="Etudiant already exists")
    etudiant = crud.ancien_etudiant.create_etudiant(schema=schema, obj_in=etudiant_in)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.put("/update_etudiant/{num_carte}", response_model=List[schemas.EtudiantAncien])
def update_etudiant(
    *,
    db: Session = Depends(deps.get_db),
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
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.get("/by_num/{schema}", response_model=schemas.EtudiantAncien)
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

@router.get("/by_mention/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_mention(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid_mention: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Get etudiant by mention.
    """
    etudiant = crud.ancien_etudiant.get_by_mention(schema=schema, uuid_mention=uuid_mention)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.get("/by_parcours/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_parcours(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid_parcours: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Get etudiant by parcours.
    """
    etudiant = crud.ancien_etudiant.get_by_parcours(schema=schema, uuid_parcours=uuid_parcours )
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours).title
            list_et.append(et)
    return list_et

@router.get("/by_semetre_and_mention/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_semstre_and_mention(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid_mention: UUID,
    semetre_grand: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Get etudiant by semestre and mention.
    """
    etudiant = crud.ancien_etudiant.get_by_semetre_and_mention(
        schema=schema, uuid_mention=uuid_mention,  semetre_grand=semetre_grand )
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.get("/by_etat/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_etat(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    etat: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Get etudiant by etat.
    """
    etudiant = crud.ancien_etudiant.get_by_etat(schema=schema, etat=etat)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.get("/by_etat_and_moyenne/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_etat_and_moyenne(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    etat: str,
    moyenne: float,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Get etudiant by etat and moyenne.
    """
    etudiant = crud.ancien_etudiant.get_by_etat_and_moyenne(schema=schema, etat=etat, moyenne=moyenne)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.get("/by_class/{schema}", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_class(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid_mention: str,
    uuid_parcours: float,
    semestre:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Get etudiant by class.
    """
    etudiant = crud.ancien_etudiant.get_by_class(schema, uuid_parcours, uuid_mention,semestre)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et

@router.delete("/{num_carte}", response_model=List[schemas.EtudiantAncien])
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
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant),cls=UUIDEncoder))
            et["parcours"]=crud.parcours.get_by_uuid(db=db,uuid=un_etudiant.uuid_parcours).title
            list_et.append(et)
    return list_et
