from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "title": "Build flask app", "completed": True},
    {"id": 2, "title": "Build a containerized app", "completed": False},
    {"id": 3, "title": "Deploy to ecs", "completed": False}
]

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html', current_time=datetime.now())

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/tasks')
def get_tasks():
    """Get all tasks"""
    return render_template('tasks.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API endpoint to get tasks as JSON"""
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    """API endpoint to add a new task"""
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "title": data.get('title', ''),
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """API endpoint to update a task"""
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = data.get('completed', task['completed'])
            task['title'] = data.get('title', task['title'])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """API endpoint to delete a task"""
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted_task = tasks.pop(i)
            return jsonify(deleted_task)
    return jsonify({"error": "Task not found"}), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

