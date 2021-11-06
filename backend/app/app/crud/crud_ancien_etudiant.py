from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from app.crud.base import CRUDBase
from app.schemas.etudiant import EtudiantAncienCreate, EtudiantAncienUpdate,EtudiantAncien
from app.db.session import engine


class CRUDEtudiantAncien(CRUDBase[EtudiantAncien, EtudiantAncienCreate, EtudiantAncienUpdate]):

    def update_etudiant(self,schema: str, num_carte: str, obj_in: EtudiantAncienUpdate) -> Optional[EtudiantAncien]:
        obj_in.num_carte = num_carte
        obj_in_data = jsonable_encoder(obj_in)
        update = text(f""" UPDATE "{schema}"."ancien_etudiant" SET 
                nom=:nom,prenom=:prenom,date_naiss=:date_naiss,lieu_naiss=:lieu_naiss,
                adresse=:adresse,sexe=:sexe,nation=:nation,
                num_cin=:num_cin,date_cin=:date_cin,lieu_cin=:lieu_cin,montant=:montant,
                num_quitance=:num_quitance,date_quitance=:date_quitance,etat=:etat,
                photo=:photo,moyenne=:moyenne,bacc=:bacc,uuid_mention=:uuid_mention,
                uuid_parcours=:uuid_parcours,uuid_semestre_petit=:uuid_semestre_petit,
                uuid_semestre_grand=:uuid_semestre_grand 
                WHERE num_carte = :num_carte 
            """)
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" """)
        with engine.begin() as con:
            con.execute(update,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row
    

    def get_by_num_carte(self, schema: str, num_carte: str) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE num_carte= :num_carte
        """)
        with engine.begin() as con:
           row = con.execute(select, {"num_carte":num_carte}).fetchone()
           return row

    def create_etudiant(self,schema: str, obj_in: EtudiantAncienCreate) -> Optional[EtudiantAncien]:
        obj_in_data = jsonable_encoder(obj_in)
        insert = text(f"""
        INSERT INTO "{schema}"."ancien_etudiant" (
            "uuid", "num_carte", "nom", "prenom", "date_naiss", "lieu_naiss", "adresse", "sexe",
            "nation", "num_cin", "date_cin","lieu_cin", "montant", "num_quitance", "date_quitance",
            "etat", "photo", "moyenne", "bacc", "uuid_mention", "uuid_parcours", "uuid_semestre_petit",
            "uuid_semestre_grand")
            VALUES
            (:uuid,:num_carte,:nom,:prenom,:date_naiss,:lieu_naiss,:adresse,:sexe,:nation,
                :num_cin,:date_cin,:lieu_cin,:montant,:num_quitance,:date_quitance,:etat,
                :photo,:moyenne,:bacc,:uuid_mention,:uuid_parcours,:uuid_semestre_petit,
                :uuid_semestre_grand); """)
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" """)
        with engine.begin() as con:
            con.execute(insert,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row

    def get_all(self,schema: str) -> Optional[EtudiantAncien]:
        insert = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant"
        """)
        with engine.begin() as con:
           row = con.execute(insert).fetchall()
           return row

    def delete_etudiant(self,schema: str, num_carte: str) -> Optional[EtudiantAncien]:
        delete = text(f"""
        DELETE FROM "{schema}"."ancien_etudiant" WHERE num_carte = :num_carte
        """)
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" """)
        with engine.begin() as con:
           con.execute(delete, {"num_carte":num_carte})
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
           return row
        


ancien_etudiant = CRUDEtudiantAncien(EtudiantAncien)
