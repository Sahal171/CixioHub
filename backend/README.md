# SmartHub Backend

## Overview

SmartHub is a productivity and knowledge management platform that provides user authentication, notes management, task management, and document management through a FastAPI backend.

## Features

* User Registration
* User Login
* JWT Authentication
* Password Hashing
* Notes CRUD Operations
* Task CRUD Operations
* Document Upload & Download
* Document Search
* User-based Access Control
* Swagger API Documentation

## Tech Stack

* FastAPI
* SQLAlchemy
* SQLite (Development)
* JWT Authentication
* Passlib (Password Hashing)
* Pydantic
* Uvicorn

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd smarthub-backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
app/
├── models/
├── schemas/
├── routers/
├── services/
├── database.py
├── dependencies.py
└── main.py

uploads/
smarthub.db
```

## Authentication

The application uses JWT-based authentication.

Protected endpoints require:

```text
Authorization: Bearer <token>
```

## Future Enhancements

* Role-Based Access Control (RBAC)
* Admin Approval Workflow
* Google OAuth Login
* OTP Verification
* PostgreSQL Migration
* RabbitMQ Notifications

## Author

Sahal Muzammil
