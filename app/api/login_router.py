from datetime import timedelta, datetime
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.dbconfig import engine, Base, get_db
from app.db import models
from app.core import secure_access
from app.schemas import schema

login = APIRouter()

@login.post("/user/auth/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(get_db)):
    
    # Cerchiamo l'utente nel database
    user = db.query(models.User).filter((models.User.username == form_data.username) | 
        (models.User.email == form_data.username)).first()
    
    # Verifichiamo se l'utente esiste e se la password è corretta
    if not user or not secure_access.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o password non corretti",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Adesso possiamo creare il token
    access_token = secure_access.generate_jwt(
        data={"sub": user.username}
    )
    
    # Restituiamo lo standard OAuth2: il token e il tipo di token (Bearer)
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
@login.post("/user/auth/logout")
def user_logout(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # pre-check per evitare operazioni inutili
    invalidated = db.query(models.InvalidToken).filter(models.InvalidToken.token == token).first()
    if not invalidated:
        # Inseriamo il token nella blacklist
        blacklisted_token = models.InvalidToken(token=token)
        db.add(blacklisted_token)
        db.commit()
    return {"message":"Logout effettuato con successo"}
