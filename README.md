# Student Task Manager Backend

A simple backend API built using Flask and SQLite to manage student tasks.  
This project demonstrates core backend concepts including REST APIs, database persistence, validation, and proper HTTP status handling.

## Features
- Create, read, update, and delete tasks (CRUD)
- SQLite database for persistent storage
- Input validation and error handling
- Protection against SQL injection using parameterized queries
- Tested using Postman

## Tech Stack
- Python
- Flask
- SQLite

## API Endpoints

### Get all tasks
GET /tasks

### Add a new task
POST /tasks  
Body:
```json
{
  "title": "Learn Flask"
}
```

## Update task status
PUT /tasks/{id}
Body:
```json
{
  "status": "done"
}
```

### Delete a task
DELETE /tasks/{id}

## How to Run Locally
- Set up virtual environment and install dependencies
- Initialize database:
```bash
python3 db_setup.py
```

## Start server:
```bash
python3 app.py
```
## Notes:
This is the initial version (v1) of the Student Task Manager backend and serves as a foundation for future features like authentication and frontend integration.
