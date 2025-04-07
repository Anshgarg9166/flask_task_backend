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

## 🧪 Sample API Usage

### Register

```bash
POST /auth/register
{
  "username": "ansh",
  "email": "ansh@example.com",
  "password": "strongpassword"
}
```

### Login

```bash
POST /auth/login
{
  "email": "ansh@example.com",
  "password": "strongpassword"
}
```

### Create Task

```bash
POST /tasks/
Authorization: Bearer <JWT_TOKEN>

{
  "task_name": "checking again task logger",
  "description": "lets see again",
  "status": true,
  "priority": "High",
  "created_at": "2024-04-06T10:00:00",
  "assigned_user": "Anshgarg"
}

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

