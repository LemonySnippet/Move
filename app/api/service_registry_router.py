from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import schema
from app.db import models
from app.db.dbconfig import get_db
from sqlalchemy.orm import Session

registry = APIRouter()

@registry.post("/service/register", response_model=schema.ServiceResponse, status_code=status.HTTP_201_CREATED)
def register_protected_service(service_in: schema.ServiceCreate, db: Session = Depends(get_db)):
    """Censisce un nuovo servizio protetto nel sistema."""
    db_service = db.query(models.ProtectedService).filter(
        models.ProtectedService.name == service_in.name
    ).first()
    
    if db_service:
        raise HTTPException(status_code=400, detail="Servizio già registrato")
    
    new_service = models.ProtectedService(
        name=service_in.name,
        service_client_id=service_in.service_client_id
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service