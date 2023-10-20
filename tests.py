import datetime
import httpx
from dotenv import load_dotenv

BASE_URL = "http://localhost:8000"

client = httpx.Client(base_url=BASE_URL)
load_dotenv()

_token = None  # Declare the token variable


def set_token(value: str) -> None:
    """Set the global token value."""
    global _token
    _token = value


def get_token() -> str:
    """Retrieve the global token value."""
    return _token


def get_headers() -> dict:
    """Generate headers with the authorization token."""
    return {"Authorization": f"Bearer {get_token()}"}


def test_create_user() -> None:
    """Test user creation endpoint."""
    response = client.post("/api/v1/users/", json={
        "username": "testuser",
        "password": "testpassword"
    })
    if response.status_code == 200:
        assert "id" in response.json()
    elif (response.status_code == 400 and "detail" in response.json() and
          response.json()["detail"] == "Username already exists"):
        pass  # If user already exists, then it's fine
    else:
        assert False, f"Unexpected response: {response.json()}"


def test_token() -> None:
    """Test token retrieval endpoint."""
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    set_token(response.json()["access_token"])


def test_create_device() -> None:
    """Test device creation endpoint."""
    response = client.post("/api/v1/devices/", headers=get_headers(), json={"name": "TestDevice"})
    assert response.status_code == 200
    assert response.json()["name"] == "TestDevice"


def test_list_devices() -> None:
    """Test device listing endpoint."""
    response = client.get("/api/v1/devices/", headers=get_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_temperature() -> None:
    """Test temperature addition endpoint."""
    response = client.post("/api/v1/temperatures/", headers=get_headers(), json={
        "temperature": 25.5,
        "timestamp": str(datetime.datetime.now())
    })
    assert response.status_code == 200


def test_latest_temperature() -> None:
    """Test latest temperature retrieval endpoint."""
    response = client.get("/api/v1/temperatures/latest/", headers=get_headers())
    assert response.status_code == 200


def test_list_temperatures() -> None:
    """Test temperature listing endpoint."""
    response = client.get("/api/v1/temperatures/", headers=get_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_temperatures_by_device_id() -> None:
    """Test temperature retrieval by device ID endpoint."""
    response = client.get("/api/v1/temperatures/by_device_id/11/", headers=get_headers())
    assert response.status_code == 200


def test_temperatures_by_device_name() -> None:
    """Test temperature retrieval by device name endpoint."""
    response = client.get("/api/v1/temperatures/by_device_name/DeviceNameVish2/", headers=get_headers())
    assert response.status_code == 200

