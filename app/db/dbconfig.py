from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# comparira' il db dentro il percorso dell'app
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# fabbrica delle nostre sessioni di database
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
