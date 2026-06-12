from app.api import register_router, login_router, service_registry_router, service_consume_router
from app.db.dbconfig import engine, Base
from app.db import models
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(register_router.register)
app.include_router(login_router.login)
app.include_router(service_registry_router.registry)
app.include_router(service_consume_router.consume)
    
