import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from httpx import AsyncClient, ASGITransport
import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.main import app
from db.session import get_session
# Import all models to ensure they're registered with SQLModel
from models.models import *

# Create a test database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"

def create_test_database():
    """Create test database and tables"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    # Create all tables
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_test_database()
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="session")
def session_fixture(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(name="client")
async def client_fixture(session: Session):
    # Override the get_session dependency
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 404

# Test adding one user successfully
@pytest.mark.anyio
async def test_add_users_success(client: AsyncClient):
   
    request_data = [{
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com"
    }]
    
    response = await client.post("/users/user", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully created 1 users"
    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "John"
    assert data["users"][0]["surname"] == "Doe"
    assert data["users"][0]["email"] == "john@example.com"
    assert "id" in data["users"][0]
    
    # Test adding two users at the same time successfully
@pytest.mark.anyio
async def test_add_users_successfully(client: AsyncClient, session: Session):
   
    request_data = [{
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com"
    },{
        "name": "Jon",
        "surname": "Doe",
        "email": "jon@example.com"
    }]
    
    response = await client.post("/users/user", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully created 2 users"
    assert len(data["users"]) == 2
    assert data["users"][0]["name"] == "John"
    assert data["users"][0]["surname"] == "Doe"
    assert data["users"][0]["email"] == "john@example.com"
    assert "id" in data["users"][0]
    assert data["users"][1]["name"] == "Jon"
    assert data["users"][1]["surname"] == "Doe"
    assert data["users"][1]["email"] == "jon@example.com"
    assert "id" in data["users"][1]

# Test adding user with duplicate email
@pytest.mark.anyio
async def test_add_users_duplicate_email(client: AsyncClient):
    # Create first user
    await client.post("/users/user", json=[{
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com"
    }])
    
    # Try to create user with same email
    response = await client.post("/users/user", json=[{
        "name": "Jane",
        "surname": "Smith",
        "email": "john@example.com"
    }])
    assert response.status_code == 400
    error_data = response.json()
    assert "Email already exists" in error_data["detail"]["message"]

# Test getting all users
@pytest.mark.anyio
async def test_get_users(client: AsyncClient):
    # Create some users
    request_data = [{
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com"
    },{
        "name": "Jon",
        "surname": "Doe",
        "email": "jon@example.com"
    }]
    
    await client.post("/users/user", json=request_data)
    
    #Get users
    response = await client.get("/users/users")
    assert response.status_code == 200
    
    users = response.json()
    assert len(users) == 2
    assert any(user["email"] == "john@example.com" for user in users)
    assert any(user["email"] == "jon@example.com" for user in users)
    
    
@pytest.mark.anyio
async def test_delete_user(client: AsyncClient):
    # Create a user first
    request_data = [{
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com"
    }]
    
    # Create the user
    create_response = await client.post("/users/user", json=request_data)
    assert create_response.status_code == 200
    created_user = create_response.json()["users"][0]
    user_id = created_user["id"]
    
    print(f"Created user with ID: {user_id}")
    
    # Delete user
    response = await client.delete(f"/users/user/{user_id}")
    assert response.status_code == 200
    
    # Verify user is deleted
    get_response = await client.get("/users/users")
    users = get_response.json()
    assert len(users) == 0