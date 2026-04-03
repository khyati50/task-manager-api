# Student Task Manager API

A secure RESTful backend API for managing student academic tasks.
Built using Flask and SQLite, featuring JWT-based authentication,
pagination, filtering, and structured API design.

---

## Features

- 🔐 JWT-based authentication with token expiry
- 📝 Full CRUD operations for task management
- 📊 Pagination and sorting for scalable data retrieval
- 🔍 Filter tasks by status (pending, in-progress, done)
- ⚡ Priority-based task organization
- 📅 Due date tracking
- 👤 User-specific data isolation (secure access)
- ✅ Robust input validation and error handling
- 🔒 Password hashing using Werkzeug

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

| Method | Endpoint    | Description                 |
| ------ | ----------- | --------------------------- |
| POST   | `/register` | Register a new user         |
| POST   | `/login`    | Login and receive JWT token |

### Tasks (Protected Routes)

| Method | Endpoint    | Description                                         |
| ------ | ----------- | --------------------------------------------------- |
| GET    | /tasks      | Get tasks (supports pagination, filtering, sorting) |
| POST   | /tasks      | Create a new task                                   |
| PATCH  | /tasks/<id> | Update task (status, title, etc.)                   |
| DELETE | /tasks/<id> | Delete a task                                       |

### Query Parameters (GET /tasks)

| Parameters | Description                                    | Default    |
| ---------- | ---------------------------------------------- | ---------- |
| page       | Page number                                    | 1          |
| limit      | Number of tasks per page (max 100)             | 10         |
| status     | Filter by task status                          | optional   |
| sort       | Sort by field (created_at, due_date, priority) | created_at |

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

### Get Tasks with Pagination

GET /tasks?page=2&limit=5&sort=due_date
Authorization: Bearer <token>

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
| ---- | ---------------------------------- |
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
- JWT tokens expire after 1 hour

---

## Author

**Khyati Anand**

- GitHub: [@khyati50](https://github.com/khyati50)
- LinkedIn: [khyati anand](https://linkedin.com/in/khyati-anand-b210b6345)
