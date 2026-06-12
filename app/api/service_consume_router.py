from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import schema
from app.db import models
from app.db.dbconfig import get_db
from app.core.secure_access import authorize_user
from sqlalchemy.orm import Session

consume = APIRouter()

@consume.get("/service/secure-data")
def get_protected_resource(current_user: str = Depends(authorize_user)):
    """
    Risorsa protetta simulata. Richiede un JWT valido nell'header come dependency injection.
    """
    return {
        "status": "success",
        "message": f"Token valido: {current_user}! Hai avuto accesso alla risorsa protetta.",
        "secret_data": [
            {"id": 1, "document": "Report Finanziario Segreto Q2"},
            {"id": 2, "document": "Documento ancora piu' segreto"}
        ]
    }