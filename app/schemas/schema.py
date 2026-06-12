from pydantic import BaseModel, EmailStr
from typing import Optional

# definisco gli schemi dati per tutto cio' che riguarda il censimento
# dell'utenza in INPUT seguendo il principio di singola responsabilita'
# delle interfacce
class UserGeneralities(BaseModel):
    username: str
    email: EmailStr

class UserPass(UserGeneralities):
    password: str

# Qui modello la risposta in OUTPUT. Facendo ereditare dal modello base
# Riesco ad evitare di censire qui dentro la password, azzerando il rischio
# di pubblicazione inavvertita della credenziale.
class UserResponse(UserGeneralities):
    id: int
    is_active: bool

    class Config:
        from_attributes=True 
        # Questo serve per far digerire a pydantic l'oggetto
        # che arriva via SQLAlchemy
# ----------------------------------------------------------------#

# Qui definisco gli elementi essenziali del servizio protetto
# valgono le medesime osservazioni tecniche fatte per gli utenti
# sempre per singola responsabilita', si mantiene la linea di eredita'
# con il modello base.
class ServiceBase(BaseModel):
    name: str

class ServiceCreate(ServiceBase):
    service_client_id: str

class ServiceResponse(ServiceBase):
    id: int
    service_client_id: str
    is_active: bool

    class Config:
        from_attributes = True