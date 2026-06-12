from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import dotenv_values
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.db import models
from app.db.dbconfig import get_db
from sqlalchemy.orm import Session

# qui devo predisporre le funzioni necessarie per criptare 
# le password e generare i JSON webtokens 

crypto_config = dotenv_values("app/core/.env")

token_key = crypto_config.get("SK")
token_encode_algo = crypto_config.get("ALGORITHM")
token_expires_after = int(crypto_config.get("TOKEN_EXPIRES"))

password_crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pwd:str) -> str:
    return password_crypto_context.hash(pwd)

def verify_password(plain:str, hashed:str) -> bool: 
    return password_crypto_context.verify(plain, hashed)

def generate_jwt(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un JSON Web Token firmato."""
    to_encode = data.copy()
    
    # data di scadenza se specifico
    # altrimenti l'env setta un default di 10 minuti
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=token_expires_after)
    
    # Inseriamo la scadenza nel payload del token (il campo standard è 'exp')
    to_encode.update({"exp": expire})
    
    # Firmiamo il token usando la nostra chiave
    encoded_jwt = jwt.encode(to_encode, token_key, algorithm=token_encode_algo)
    return encoded_jwt

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/login")
# Questa eccezione salta solo se il token per qualche motivo non va bene
# oppure non esiste, oppure lo user e' malformato.
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenziali non valide o token scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )

def authorize_user(token: str = Depends(oauth_scheme), 
                    db: Session = Depends(get_db)) -> str:
    
    is_blacklisted = db.query(models.InvalidToken).filter(models.InvalidToken.token == token).first()
    if is_blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Questo token è stato invalidato (logout effettuato).",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, token_key, algorithms=[token_encode_algo])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
