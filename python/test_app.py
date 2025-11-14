import pytest
from app import app, tasks


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home page"""
    response = client.get('/')
    assert response.status_code == 200


def test_about(client):
    """Test the about page"""
    response = client.get('/about')
    assert response.status_code == 200


def test_tasks(client):
    """Test the tasks page"""
    response = client.get('/tasks')
    assert response.status_code == 200


def test_api_get_tasks(client):
    """Test the API endpoint to get tasks"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_api_add_task(client):
    """Test the API endpoint to add a task"""
    new_task = {"title": "Test task"}
    response = client.post('/api/tasks', json=new_task)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Test task"
    assert data['completed'] is False


def test_api_update_task(client):
    """Test the API endpoint to update a task"""
    update_data = {"completed": True, "title": "Updated task"}
    response = client.put('/api/tasks/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['completed'] is True


def test_api_update_task_not_found(client):
    """Test updating a non-existent task"""
    update_data = {"completed": True}
    response = client.put('/api/tasks/9999', json=update_data)
    assert response.status_code == 404


def test_api_delete_task(client):
    """Test the API endpoint to delete a task"""
    response = client.delete('/api/tasks/2')
    assert response.status_code == 200


def test_api_delete_task_not_found(client):
    """Test deleting a non-existent task"""
    response = client.delete('/api/tasks/9999')
    assert response.status_code == 404


def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404

