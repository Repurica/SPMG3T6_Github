import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'running!!' in response.data

def test_all_employee(client):
    response = client.get('/sample/all_employee ')
    assert response.status_code == 200


def test_one_employee(client):
    response = client.get('/sample/one_employee?id=140001')
    assert response.status_code == 200
    # assert b'running!!' in response.data

# def test_about_page(client):
#     response = client.get('/about')
#     assert response.status_code == 200
#     assert b'About Us' in response.data

# def test_create_post(client):
#     response = client.post('/post', data={'title': 'Test Post', 'content': 'This is a test'})
#     assert response.status_code == 302  # Assuming a redirect after successful post creation
    
#     # Check if the post was actually created
#     response = client.get('/posts')
#     assert b'Test Post' in response.data

# def test_invalid_page(client):
#     response = client.get('/invalid_page')
#     assert response.status_code == 404