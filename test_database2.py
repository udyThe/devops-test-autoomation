import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from bson import ObjectId
from apiserver2 import app

# Mock data for testing
MOCK_DATA = [
    {
        "_id": ObjectId("5f8d8b7e4e3a2b1c9c8b4567"),
        "operation": "add",
        "num1": 2,
        "num2": 3,
        "result": 5
    },
    {
        "_id": ObjectId("5f8d8b7e4e3a2b1c9c8b4568"),
        "operation": "subtract",
        "num1": 5,
        "num2": 3,
        "result": 2
    }
]

@pytest.fixture
def mock_collection():
    """Mock MongoDB collection with async methods"""
    collection = AsyncMock()
    
    # Mock find() to return our test data
    async def mock_find(*args, **kwargs):
        for doc in MOCK_DATA:
            yield doc
    
    collection.find = mock_find
    
    # Mock insert_one() to return a mock result
    async def mock_insert_one(document):
        return MagicMock(inserted_id=ObjectId())
    
    collection.insert_one = mock_insert_one
    
    return collection

@pytest.fixture
def test_client(mock_collection):
    """TestClient fixture with mocked database"""
    with patch('apiserver2.collection', mock_collection):
        yield TestClient(app)

# Test cases
def test_root_endpoint(test_client):
    """Test the root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Math API with MongoDB Atlas"}

def test_add_operation(test_client):
    """Test the addition endpoint"""
    response = test_client.post("/add/2/3")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "result" in data
    assert data["result"] == 5
    assert ObjectId.is_valid(data["id"])

def test_subtract_operation(test_client):
    """Test the subtraction endpoint"""
    response = test_client.post("/subtract/5/3")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "result" in data
    assert data["result"] == 2
    assert ObjectId.is_valid(data["id"])

def test_multiply_operation(test_client):
    """Test the multiplication endpoint"""
    response = test_client.post("/multiply/2/3")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "result" in data
    assert data["result"] == 6
    assert ObjectId.is_valid(data["id"])

def test_history_endpoint(test_client):
    """Test the history endpoint"""
    response = test_client.get("/history/")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert len(data["history"]) == len(MOCK_DATA)
    for item in data["history"]:
        assert "id" in item
        assert "operation" in item
        assert "num1" in item
        assert "num2" in item
        assert "result" in item

# Test error cases
def test_invalid_input(test_client):
    """Test invalid input handling"""
    response = test_client.post("/add/foo/bar")
    assert response.status_code == 422  # Validation error
    assert "detail" in response.json()



# Test direct function calls (unit test style)
@pytest.mark.asyncio
async def test_add_function(mock_collection):
    """Test the add function directly"""
    from apiserver2 import add
    with patch('apiserver2.collection', mock_collection):
        result = await add(2, 3)
        assert result["result"] == 5
        assert ObjectId.is_valid(result["id"])