# Student Task Manager API

A RESTful backend API for managing student academic tasks, built using Flask and SQLite.  
This project demonstrates core backend concepts such as authentication, authorization, database design, and clean API structure.

---

## Features

- 🔐 User authentication using JWT (JSON Web Tokens)
- 📝 Create, read, update, and delete tasks (CRUD)
- 📅 Due dates for tasks
- ⚡ Priority levels (low, medium, high)
- 📚 Subject/course tagging for tasks
- 🔍 Filter tasks by status (pending, in-progress, done)
- 👤 Tasks are user-specific (no cross-user access)

---

## Tech Stack

- Python 3
- Flask
- SQLite
- PyJWT (JWT authentication)
- Werkzeug (password hashing)
- Flask-CORS

---

## Authentication Flow

1. User registers using `/register`
2. User logs in using `/login`
3. A JWT token is returned on successful login
4. This token must be included in the `Authorization` header for all protected routes

**Authorization Header Format:**
```
Authorization: Bearer <your-jwt-token>
```

---

## API Endpoints

### Authentication

| Method | Endpoint    | Description                  |
|--------|-------------|------------------------------|
| POST   | `/register` | Register a new user          |
| POST   | `/login`    | Login and receive JWT token  |

### Tasks (Protected Routes)

| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| GET    | `/tasks`                | Get all tasks                    |
| GET    | `/tasks?status=pending` | Filter tasks by status           |
| POST   | `/tasks`                | Create a new task                |
| PUT    | `/tasks/<id>`           | Update task (title/status/etc.)  |
| DELETE | `/tasks/<id>`           | Delete a task                    |

---

## Request Examples

### Register User
```json
POST /register
{
  "username": "student1",
  "password": "mypassword"
}
```

### Login
```json
POST /login
{
  "username": "student1",
  "password": "mypassword"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create Task
```json
POST /tasks
Authorization: Bearer <token>

{
  "title": "Math Assignment",
  "subject": "Mathematics",
  "priority": "high",
  "due_date": "2026-01-30"
}
```

### Update Task
```json
PUT /tasks/1
Authorization: Bearer <token>

{
  "status": "done"
}
```

---

## Status Codes

| Code | Meaning                            |
|------|------------------------------------|
| 200  | Success                            |
| 201  | Created successfully               |
| 400  | Bad request (invalid input)        |
| 401  | Unauthorized (not logged in)       |
| 404  | Resource not found                 |
| 409  | Conflict (username already exists) |

---

## Project Structure

```
student-task-manager/
├── app.py           # Main Flask application
├── db.py            # Database operations
├── db_setup.py      # Database initialization
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
├── .env             # Environment variables (not in repo)
├── .gitignore       # Git ignore file
└── README.md        # Documentation
```

---

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/student-task-manager.git
   cd student-task-manager
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   echo "SECRET_KEY=your-secret-key-here" > .env
   ```

5. **Initialize database**
   ```bash
   python3 db_setup.py
   ```

6. **Run the application**
   ```bash
   python3 app.py
   ```

7. **Server will start at:** `http://127.0.0.1:5000`

---

## Notes

- This is a backend-only project (frontend coming soon)
- Secrets are managed using environment variables (`.env`)
- SQLite is used for simplicity and learning purposes
- All task routes are protected and require JWT authentication

---

## Author

**Your Name**  
- GitHub: [@khyati50](https://github.com/khyati50)
- LinkedIn: [khyati anand](https://linkedin.com/in/khyati-anand-b210b6345)
