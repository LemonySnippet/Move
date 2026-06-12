from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Indichiamo a SQLite dove salvare il file del database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 'connect_args' serve solo a SQLite per permettere a più thread di accedere allo stesso DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Questa oggetto sarà la fabbrica delle nostre sessioni di database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base da cui erediteranno tutti i nostri modelli ORM
Base = declarative_base()

# Dependency Injection per FastAPI: apre una sessione per ogni richiesta 
# e la chiude alla fine
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()