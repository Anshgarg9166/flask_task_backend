# 📝 Flask Task Management API

A robust, production-ready Task Management API built with **Flask**, supporting JWT-based authentication, role-based access control, background tasks with Celery, rate-limiting, and Redis caching.

---

## 👤 Author

**Ansh Garg**

---

## 📁 Project Structure

```
flask_task_backend/
│
├── app/
│   ├── __init__.py          # Flask app factory setup
│   ├── config/              # Environment configurations (dev, prod, staging)
│   ├── extensions.py        # DB, JWT, cache, limiter setup
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── logger.py
│   │   └── events.py
│   ├── routes/              # Blueprints for API routes
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── tasks/               # Celery background tasks
│   │   └── daily_log.py
│   └── celery.py            # Celery factory function
│
├── migrations/              # Flask-Migrate DB migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py                   # Entrypoint for running Flask app
├── README.md
└── .env.dev/.env.prod/.env.staging
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Anshgarg9166/flask_task_backend.git
cd flask_task_backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env.dev` file at the root with:

```env
SECRET_KEY=supersecret
JWT_SECRET_KEY=anothersecret
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/task_db
REDIS_HOST=localhost
REDIS_PORT=6379
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Also create `.env.prod` and `.env.staging` with respective configurations.

### 5. Run DB Migrations

```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

### 6. Run the App

```bash
flask run
```

### 7. Run Celery Worker

```bash
celery -A app.celery worker --loglevel=info
```

---

## 🐳 Docker Setup (Optional)

### 1. Build and Start Containers

```bash
docker-compose up --build
```

### 2. Access Services

- Flask API: [http://localhost:5000](http://localhost:5000)
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 3. Troubleshooting

If PostgreSQL throws a version mismatch error:

```bash
# Stop containers
docker-compose down

# Remove volume manually
docker volume rm flask_task_backend_postgres_data

# Rebuild
docker-compose up --build
```

---

## 🌐 API Reference

### 🔐 Authentication Routes

| Endpoint         | Method | Description                 |
| ---------------- | ------ | --------------------------- |
| `/auth/register` | POST   | Register a new user         |
| `/auth/login`    | POST   | Login and receive JWT token |
| `/auth/users`    | GET    | List all users (Admin only) |

### ✅ Task Management Routes

| Endpoint                                         | Method | Description                                            |
| ------------------------------------------------ | ------ | ------------------------------------------------------ |
| `/tasks/`                                        | GET    | Greeting message from task service                     |
| `/tasks/`                                        | POST   | Create a new task                                      |
| `/tasks/list`                                    | GET    | List all tasks for the current user                    |
| `/tasks/by-date?start=YYYY-MM-DD&end=YYYY-MM-DD` | GET    | Fetch tasks within a given date range                  |
| `/tasks/<int:task_logger_id>`                    | GET    | Get task details for a specific task log entry         |
| `/tasks/<int:task_id>`                           | PUT    | Update task details (Admin or task creator only)       |
| `/tasks/<int:task_id>`                           | DELETE | Soft delete a task (mark inactive instead of removing) |
| `/tasks/upload-csv`                              | POST   | Bulk upload tasks from a CSV file                      |

---

## 📬 API Endpoints & Sample Requests

### 🔐 Auth

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "username": "ansh123",
  "email": "ansh@example.com",
  "password": "strongpassword"
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "ansh@example.com",
  "password": "strongpassword"
}
```

#### List Users (Admin only)
```
GET /auth/users
Authorization: Bearer <JWT_TOKEN>
```

---

### 📋 Tasks

#### Create Task
```
POST /tasks/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "New Task",
  "description": "Description of task",
  "due_date": "2025-04-10"
}
```

#### Tasks Greeting
```
GET /tasks/
```

#### Update Task
```
PUT /tasks/<task_id>
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated description",
  "due_date": "2025-04-15"
}
```

#### Delete Task (Soft Delete)
```
DELETE /tasks/<task_id>
Authorization: Bearer <JWT_TOKEN>
```

#### Get Task Details
```
GET /tasks/<task_logger_id>
Authorization: Bearer <JWT_TOKEN>
```

#### List All Tasks
```
GET /tasks/list
Authorization: Bearer <JWT_TOKEN>
```

#### Get Tasks by Date
```
GET /tasks/by-date?date=2025-04-10
Authorization: Bearer <JWT_TOKEN>
```

#### Upload CSV
```
POST /tasks/upload-csv
Authorization: Bearer <JWT_TOKEN>
Content-Type: multipart/form-data
file: [Upload CSV file]
```

---

## 📌 Tech Stack

- Python 3.11
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Celery + Redis
- PostgreSQL
- Docker & Docker Compose

---

## 📄 License

This project is licensed under the MIT License.

---

**Made with ❤️ by Ansh Garg**

