import pytest
from starlette.testclient import TestClient as TestClient
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Importiamo la tua app, la Base dei modelli e la dipendenza del DB
from main import app
from app.db.dbconfig import Base, get_db

# db dedicato ai test per non sporcare quello ufficiale
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    # Mocka praticamente lo stesso processo dell'app
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(session):
    # passiamo la fixture anziche' usare la funzione originale
    def override_get_db():
        try:
            yield session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Finiti i test, puliamo le sostituzioni dell'app
    app.dependency_overrides.clear()


# TESTS

def test_full_auth_flow(client):
    """
    Test end-to-end:
    Registrazione -> Login -> Accesso Protetto -> Logout -> Blocco Accesso
    """
    
    # REGISTRAZIONE
    payload_register = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "supersecretpassword"
    }
    response_reg = client.post("/user/auth/register", json=payload_register)
    assert response_reg.status_code == 201
    data_reg = response_reg.json()
    assert data_reg["username"] == "testuser"
    assert "password" not in data_reg  # Verifichiamo che la password sia effettivamente nascosta
    assert "id" in data_reg

    # LOGIN
    payload_login = {
        "username": "testuser",
        "password": "supersecretpassword"
    }
    response_log = client.post("/user/auth/login", data=payload_login)
    assert response_log.status_code == 200
    data_log = response_log.json()
    assert "access_token" in data_log
    assert data_log["token_type"] == "bearer"
    
    token = data_log["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # RISORSA PROTETTA BLOCCATA SE NO TOKEN
    response_protected_fail = client.get("/service/secure-data")
    assert response_protected_fail.status_code == 401

    # RISORSA PROTETTA OPEN SE TOKEN VALIDO
    response_protected_success = client.get("/service/secure-data", headers=headers)
    assert response_protected_success.status_code == 200
    data_protected = response_protected_success.json()
    assert data_protected["status"] == "success"
    assert "testuser" in data_protected["message"]

    # LOGOUT
    response_logout = client.post("/user/auth/logout", headers=headers)
    assert response_logout.status_code == 200
    assert "Logout effettuato" in response_logout.json()["message"]

    # RISORSA PROTETTA BLOCCATA SE TOKEN SLOGGATO
    response_post_logout = client.get("/service/secure-data", headers=headers)
    assert response_post_logout.status_code == 401
    assert "invalidato" in response_post_logout.json()["detail"]

# NO USER DUPLICATI
def test_register_duplicate_username(client):
    # mail diversa allora username uguale non accettabile.
    user_data = {"username": "nomedoppio", "email": "1@ex.com", "password": "123"}
    
    # Primo inserimento
    res1 = client.post("/user/auth/register", json=user_data)
    assert res1.status_code == 201
    
    # Secondo inserimento con stessa username (ma email diversa)
    user_data["email"] = "2@ex.com"
    res2 = client.post("/user/auth/register", json=user_data)
    assert res2.status_code == 400
    assert "Username esistente" in res2.json()["detail"]