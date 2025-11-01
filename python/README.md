# Simple Python Web App

A simple Flask-based web application demonstrating basic web development concepts including:
- Multiple routes and pages
- Template rendering
- RESTful API endpoints
- Static file serving
- Error handling

## Features

- **Home Page**: Welcome page with current server time
- **About Page**: Information about the application
- **Tasks Page**: Interactive task list manager
- **REST API**: CRUD operations for tasks

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Navigate to the project directory:
```bash
cd /Users/gaurav.dhapola/Documents/DevOps/python
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
# venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### Get All Tasks
```bash
GET /api/tasks
```

### Add New Task
```bash
POST /api/tasks
Content-Type: application/json

{
  "title": "New task"
}
```

### Update Task
```bash
PUT /api/tasks/<task_id>
Content-Type: application/json

{
  "title": "Updated task",
  "completed": true
}
```

### Delete Task
```bash
DELETE /api/tasks/<task_id>
```

## Project Structure

```
python/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── tasks.html
│   └── 404.html
└── static/           # Static files (CSS, JS)
    └── style.css
```

## Development

To run in debug mode (auto-reload on code changes):
```bash
export FLASK_ENV=development
python app.py
```

## License

MIT License

