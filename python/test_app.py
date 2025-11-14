import pytest
from datetime import datetime
from app import app, tasks


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_tasks():
    """Reset tasks to initial state before each test"""
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Build flask app", "completed": True},
        {"id": 2, "title": "Build a containerized app", "completed": False},
        {"id": 3, "title": "Deploy to ecs", "completed": False}
    ])
    yield
    # Cleanup after test
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Build flask app", "completed": True},
        {"id": 2, "title": "Build a containerized app", "completed": False},
        {"id": 3, "title": "Deploy to ecs", "completed": False}
    ])


class TestHomeRoute:
    """Test cases for home route"""

    def test_home_status_code(self, client):
        """Test that home page returns 200 status code"""
        response = client.get('/')
        assert response.status_code == 200

    def test_home_content(self, client):
        """Test that home page contains expected content"""
        response = client.get('/')
        assert b'Gaurav Dhapola' in response.data
        assert b'Flask-based containerized application' in response.data

    def test_home_current_time(self, client):
        """Test that home page displays current time"""
        response = client.get('/')
        # Check that the response contains a date in the expected format
        current_year = str(datetime.now().year)
        assert current_year.encode() in response.data

    def test_home_links(self, client):
        """Test that home page contains navigation links"""
        response = client.get('/')
        assert b'/tasks' in response.data
        assert b'/about' in response.data


class TestAboutRoute:
    """Test cases for about route"""

    def test_about_status_code(self, client):
        """Test that about page returns 200 status code"""
        response = client.get('/about')
        assert response.status_code == 200

    def test_about_content(self, client):
        """Test that about page contains expected content"""
        response = client.get('/about')
        assert b'About This Application' in response.data
        assert b'Flask' in response.data
        assert b'Python 3' in response.data
        assert b'AWS ECS' in response.data

    def test_about_technologies(self, client):
        """Test that about page lists technologies"""
        response = client.get('/about')
        assert b'Technologies Used' in response.data
        assert b'REST API' in response.data


class TestTasksRoute:
    """Test cases for tasks route"""

    def test_tasks_status_code(self, client):
        """Test that tasks page returns 200 status code"""
        response = client.get('/tasks')
        assert response.status_code == 200

    def test_tasks_displays_all_tasks(self, client):
        """Test that tasks page displays all tasks"""
        response = client.get('/tasks')
        assert b'Build flask app' in response.data
        assert b'Build a containerized app' in response.data
        assert b'Deploy to ecs' in response.data


class TestApiGetTasks:
    """Test cases for GET /api/tasks endpoint"""

    def test_api_get_tasks_status_code(self, client):
        """Test that API returns 200 status code"""
        response = client.get('/api/tasks')
        assert response.status_code == 200

    def test_api_get_tasks_returns_list(self, client):
        """Test that API returns a list"""
        response = client.get('/api/tasks')
        data = response.get_json()
        assert isinstance(data, list)

    def test_api_get_tasks_count(self, client):
        """Test that API returns correct number of tasks"""
        response = client.get('/api/tasks')
        data = response.get_json()
        assert len(data) == 3

    def test_api_get_tasks_structure(self, client):
        """Test that each task has correct structure"""
        response = client.get('/api/tasks')
        data = response.get_json()
        for task in data:
            assert 'id' in task
            assert 'title' in task
            assert 'completed' in task

    def test_api_get_tasks_content(self, client):
        """Test that API returns correct task data"""
        response = client.get('/api/tasks')
        data = response.get_json()
        assert data[0]['title'] == "Build flask app"
        assert data[0]['completed'] is True
        assert data[1]['completed'] is False


class TestApiAddTask:
    """Test cases for POST /api/tasks endpoint"""

    def test_api_add_task_success(self, client):
        """Test adding a new task successfully"""
        new_task = {"title": "Test task"}
        response = client.post('/api/tasks', json=new_task)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == "Test task"
        assert data['completed'] is False
        assert 'id' in data

    def test_api_add_task_increments_id(self, client):
        """Test that new task gets correct ID"""
        initial_count = len(tasks)
        new_task = {"title": "New task"}
        response = client.post('/api/tasks', json=new_task)
        data = response.get_json()
        assert data['id'] == initial_count + 1

    def test_api_add_task_without_title(self, client):
        """Test adding task without title"""
        response = client.post('/api/tasks', json={})
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == ''
        assert data['completed'] is False

    def test_api_add_task_empty_title(self, client):
        """Test adding task with empty title"""
        new_task = {"title": ""}
        response = client.post('/api/tasks', json=new_task)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == ""

    def test_api_add_task_persists(self, client):
        """Test that added task persists in tasks list"""
        initial_count = len(tasks)
        new_task = {"title": "Persistent task"}
        client.post('/api/tasks', json=new_task)
        assert len(tasks) == initial_count + 1
        assert tasks[-1]['title'] == "Persistent task"

    def test_api_add_multiple_tasks(self, client):
        """Test adding multiple tasks"""
        task1 = {"title": "Task 1"}
        task2 = {"title": "Task 2"}
        
        response1 = client.post('/api/tasks', json=task1)
        response2 = client.post('/api/tasks', json=task2)
        
        assert response1.status_code == 201
        assert response2.status_code == 201
        assert response1.get_json()['id'] != response2.get_json()['id']


class TestApiUpdateTask:
    """Test cases for PUT /api/tasks/<id> endpoint"""

    def test_api_update_task_completed_status(self, client):
        """Test updating task completion status"""
        update_data = {"completed": True}
        response = client.put('/api/tasks/2', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['completed'] is True
        assert data['id'] == 2

    def test_api_update_task_title(self, client):
        """Test updating task title"""
        update_data = {"title": "Updated task title"}
        response = client.put('/api/tasks/1', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == "Updated task title"

    def test_api_update_task_both_fields(self, client):
        """Test updating both title and completed status"""
        update_data = {"completed": True, "title": "Completely updated"}
        response = client.put('/api/tasks/3', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['completed'] is True
        assert data['title'] == "Completely updated"

    def test_api_update_task_not_found(self, client):
        """Test updating non-existent task"""
        update_data = {"completed": True}
        response = client.put('/api/tasks/9999', json=update_data)
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "Task not found"

    def test_api_update_task_persists(self, client):
        """Test that task update persists"""
        update_data = {"completed": True}
        client.put('/api/tasks/2', json=update_data)
        # Verify the change persisted
        task = next((t for t in tasks if t['id'] == 2), None)
        assert task is not None
        assert task['completed'] is True

    def test_api_update_task_partial_update(self, client):
        """Test partial update keeps existing values"""
        original_title = tasks[0]['title']
        update_data = {"completed": False}
        response = client.put('/api/tasks/1', json=update_data)
        data = response.get_json()
        assert data['title'] == original_title

    def test_api_update_task_empty_json(self, client):
        """Test updating task with empty JSON"""
        response = client.put('/api/tasks/1', json={})
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data


class TestApiDeleteTask:
    """Test cases for DELETE /api/tasks/<id> endpoint"""

    def test_api_delete_task_success(self, client):
        """Test deleting a task successfully"""
        initial_count = len(tasks)
        response = client.delete('/api/tasks/2')
        assert response.status_code == 200
        assert len(tasks) == initial_count - 1

    def test_api_delete_task_returns_deleted_task(self, client):
        """Test that delete returns the deleted task"""
        response = client.delete('/api/tasks/1')
        data = response.get_json()
        assert data['id'] == 1
        assert data['title'] == "Build flask app"

    def test_api_delete_task_not_found(self, client):
        """Test deleting non-existent task"""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "Task not found"

    def test_api_delete_task_removes_from_list(self, client):
        """Test that deleted task is removed from list"""
        client.delete('/api/tasks/2')
        task_ids = [t['id'] for t in tasks]
        assert 2 not in task_ids

    def test_api_delete_multiple_tasks(self, client):
        """Test deleting multiple tasks"""
        initial_count = len(tasks)
        client.delete('/api/tasks/1')
        client.delete('/api/tasks/2')
        assert len(tasks) == initial_count - 2

    def test_api_delete_last_task(self, client):
        """Test deleting the last task in list"""
        response = client.delete('/api/tasks/3')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 3


class TestErrorHandling:
    """Test cases for error handling"""

    def test_404_error_handler(self, client):
        """Test custom 404 error handler"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
        assert b'404' in response.data

    def test_404_error_content(self, client):
        """Test 404 page content"""
        response = client.get('/this-page-does-not-exist')
        assert response.status_code == 404
        assert b'Page Not Found' in response.data

    def test_404_error_various_routes(self, client):
        """Test 404 for various non-existent routes"""
        routes = ['/random', '/api/invalid', '/test/path']
        for route in routes:
            response = client.get(route)
            assert response.status_code == 404

    def test_404_has_home_link(self, client):
        """Test that 404 page has link to home"""
        response = client.get('/invalid')
        assert b'Go Home' in response.data or b'/' in response.data


class TestIntegration:
    """Integration test cases"""

    def test_complete_crud_workflow(self, client):
        """Test complete CRUD workflow"""
        # Create
        new_task = {"title": "Integration test task"}
        create_response = client.post('/api/tasks', json=new_task)
        assert create_response.status_code == 201
        task_id = create_response.get_json()['id']
        
        # Read
        read_response = client.get('/api/tasks')
        assert read_response.status_code == 200
        task_exists = any(t['id'] == task_id for t in read_response.get_json())
        assert task_exists
        
        # Update
        update_response = client.put(f'/api/tasks/{task_id}', 
                                     json={"completed": True})
        assert update_response.status_code == 200
        assert update_response.get_json()['completed'] is True
        
        # Delete
        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 200

    def test_task_lifecycle(self, client):
        """Test task from creation to completion to deletion"""
        # Create task
        task_data = {"title": "Lifecycle task"}
        response = client.post('/api/tasks', json=task_data)
        task_id = response.get_json()['id']
        
        # Mark as completed
        client.put(f'/api/tasks/{task_id}', json={"completed": True})
        
        # Verify completion
        tasks_response = client.get('/api/tasks')
        task = next((t for t in tasks_response.get_json() if t['id'] == task_id), None)
        assert task['completed'] is True
        
        # Delete
        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 200

    def test_api_consistency(self, client):
        """Test that API and web routes show same data"""
        # Get data from API
        api_response = client.get('/api/tasks')
        api_tasks = api_response.get_json()
        
        # Get web page
        web_response = client.get('/tasks')
        
        # Verify all API tasks appear on web page
        for task in api_tasks:
            assert task['title'].encode() in web_response.data


class TestDataValidation:
    """Test cases for data validation"""

    def test_task_id_is_integer(self, client):
        """Test that task IDs are integers"""
        response = client.get('/api/tasks')
        data = response.get_json()
        for task in data:
            assert isinstance(task['id'], int)

    def test_task_completed_is_boolean(self, client):
        """Test that completed field is boolean"""
        response = client.get('/api/tasks')
        data = response.get_json()
        for task in data:
            assert isinstance(task['completed'], bool)

    def test_task_title_is_string(self, client):
        """Test that title field is string"""
        response = client.get('/api/tasks')
        data = response.get_json()
        for task in data:
            assert isinstance(task['title'], str)

