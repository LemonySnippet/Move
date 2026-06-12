from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import timedelta, datetime, timezone
from app.db.dbconfig import Base

# devo definire le strutture dati in gioco
# avro' bisogno di una tavola per gli utenti 
# e di una tavola per il servizio protetto

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class ProtectedService(Base):
    __tablename__ = "protected_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    # Una chiave segreta condivisa o un identificativo che il servizio userà per presentarsi
    service_client_id = Column(String, unique=True, nullable=False) 
    is_active = Column(Boolean, default=True)

class InvalidToken(Base):
    __tablename__ = "invalidated_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    invalidated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))