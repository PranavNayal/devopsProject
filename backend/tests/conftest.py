import os
import pytest

# Force SQLite in-memory test database before app imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.db as db_module
import app.main as main_module
from app.db import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Point both engine references to test_engine so startup creates tables in test DB
db_module.engine = test_engine
main_module.engine = test_engine

@pytest.fixture(autouse=True)
def setup_test_db():
    """Create fresh database schema in-memory for each test and drop it afterwards."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(setup_test_db):
    """Provide isolated transactional session."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency pointing to isolated test DB."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
