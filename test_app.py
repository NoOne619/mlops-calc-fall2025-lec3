import pytest
from app import app  # import your Flask app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    with app.test_client() as client:
        yield client


def test_home_redirects_to_login(client):
    response = client.get("/")
    assert response.status_code == 302  # Redirect
    assert "/login" in response.headers["Location"]


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data  # login.html should have "Login"


def test_successful_login(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Login successful!" in response.data
    assert b"welcome" in response.data.lower()


def test_failed_login(client):
    response = client.post(
        "/login",
        data={"username": "wrong", "password": "bad"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data


def test_protected_welcome_requires_login(client):
    response = client.get("/welcome", follow_redirects=True)
    assert b"Please log in first." in response.data


def test_logout(client):
    # First login
    client.post(
        "/login",
        data={"username": "admin", "password": "password123"},
        follow_redirects=True,
    )
    # Then logout
    response = client.get("/logout", follow_redirects=True)
    assert b"You have been logged out." in response.data


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data  # about.html should contain "About"


def test_hello_page(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert b"Hello" in response.data  # hello.html should contain "Hello"
