from datetime import timedelta
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.dbconfig import engine, Base, get_db
from app.db import models
from app.core import secure_access
from app.schemas import schema

register = APIRouter()

@register.post("/user/auth/register", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
def user_registration(input_data: schema.UserPass, db: Session = Depends(get_db)):
    # prima azione: controllo se l'utente ha usato uno user/email gia'registrato
    db_user_username = db.query(models.User).filter(models.User.username == input_data.username).first()
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username esistente")
    
    db_user_email = db.query(models.User).filter(models.User.email == input_data.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="email esistente")

    # seconda azione: hash della password 
    hashed_pwd = secure_access.hash_password(input_data.password)

    # terza azione: preparo il blocco dati da mettere su db e lo aggiungo
    new_user = models.User(
        username = input_data.username,
        email=input_data.email,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user