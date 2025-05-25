
# Event Scheduling API (Django + DRF)

A collaborative event scheduling API built with Django & Django REST Framework. Designed for teams to manage events with advanced features like role-based access control, version history, diff check between versions, rollback, and sharing.

---

# FEATURES

- User authentication with JWT
- Create, read, update, delete events
- Batch event creation
- Role-based permissions (OWNER, EDITOR, VIEWER)
- Event sharing and permission management
- Version history and rollback
- Compare differences between versions
- Event changelogs
- Optimized with caching for permission lists
- Auto-generated Swagger and Redoc docs
- Lightweight setup using SQLite (dev)

---

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **SQLite (default)**
- **JWT (SimpleJWT)**
- **drf-yasg (Swagger Docs)**
- **django-simple-history (Versioning)**

---


## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/ateebaijaz/event-scheduler-backend
```

2. **Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```


5. **Run the server**

```bash
python manage.py runserver
```

---

## 🔐 Authentication (JWT)

**Obtain Token:**

```http
POST /api/auth/register
{
  "username": "your_username",
  "email" : "email",
  "password": "your_password"
}
```
In response you get 
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODY5NDcyNSwiaWF0IjoxNzQ4MDg5OTI1LCJqdGkiOiI4NjUxYjFjZTQ0ODI0NDU5YTdlMTUxZDM5NTViOTA5OCIsInVzZXJfaWQiOjExfQ.8qqYgzq_xEBmjjKcncOF9Wn1rlNSU5mF_MS53S2WasA",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4MDkzNTI1LCJpYXQiOjE3NDgwODk5MjUsImp0aSI6IjczNjdlZjQ4YzI4MTQxOWFhMzc1NmQ2NTQ0NDg3Y2ZlIiwidXNlcl9pZCI6MTF9.2sEqw20CUsU28JhR80lwsWR5pBY5HNUfTeQfBw6a-9M",
    "user": {
        "id": 11,
        "username": "ssss"
    }
}

USE ACCESS TOKEN IN AUTHORIZATION IN HEADERS OF ALL APIS ------- Bearer <access_token>
**Use in headers:**

```
Authorization: Bearer <access_token>
```

---

## 🔗 API Endpoints

### 📅 Events

- POST   /api/events — Create a new event  
- GET    /api/events — List all events accessible by the user (pagination/filtering supported)  
- GET    /api/events/{id} — Get details of a specific event  
- PUT    /api/events/{id} — Update event details  
- DELETE /api/events/{id} — Delete an event  
- POST   /api/events/batch — Bulk-create events  

### 👥 Collaboration

- POST   /api/events/{id}/share — Share an event with users and assign roles  
- GET    /api/events/{id}/permissions — List participants and their roles  
- PUT    /api/events/{id}/permissions/{userId} — Update a user's permission  
- DELETE /api/events/{id}/permissions/{userId} — Revoke a user's access  

### 🕓 Version History

- GET  /api/events/{id}/history/{versionId} — Get a specific version of an event  
- POST /api/events/{id}/rollback/{versionId} — Rollback to a previous version  

### 🧾 Changelog & Diff

- GET /api/events/{id}/changelog — View chronological log of all changes  
- GET /api/events/{id}/diff/{versionId1}/{versionId2} — Get differences between two versions  

---

## 📑 API Documentation

- Swagger: http://localhost:8000/swagger/  
- Redoc: http://localhost:8000/redoc/  

---

## 🗃️ Database

- Default: SQLite  

---

## 📄 License

MIT License — free to use and modify.

---

## Contribution

Feel free to fork this project and submit a pull request with improvements, bug fixes, or new features.
