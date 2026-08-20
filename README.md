# Gym Management System

A full-stack **Gym Management System** designed to help gym administrators manage members, memberships, payments, attendance, trainers, staff, expenses, reminders, and financial performance from a centralized dashboard.

The system provides a modern React-based admin interface backed by a RESTful FastAPI API and PostgreSQL database. It also includes automated database migrations, backend testing, and a GitHub Actions CI pipeline.

## 🚀 Features

### 📊 Admin Dashboard

The dashboard provides an overview of the gym's current operations and financial performance, including:

* Total Members
* Active Members
* Total Memberships
* Expired Memberships
* Total Trainers
* Today's Attendance
* Today's Revenue
* Today's Expenses
* Today's Profit
* Monthly Revenue
* Monthly Expenses
* Monthly Profit
* Annual Revenue
* Annual Expenses
* Annual Profit
* Memberships Expiring Soon
* Daily Financial Summary

### 👥 Member Management

* Add new members
* View member records
* Manage member information
* Track active/inactive members
* Assign memberships
* Monitor membership status

### 🎫 Membership Management

* Create membership packages
* Define package duration and pricing
* Assign memberships to members
* Track membership start and expiry dates
* Identify expired memberships
* Identify memberships expiring soon

### 💳 Payment Management

* Record member payments
* Track payment methods
* Store payment references
* View payment history
* View payments associated with individual members
* Integrate payment information with financial reporting

### 🏋️ Trainer Management

* Add trainers
* Manage trainer information
* Track specialization
* Manage trainer salaries
* Track active/inactive trainers

### 👨‍💼 Staff Management

* Add gym staff
* Manage staff information
* Define staff roles
* Track salaries
* Track active/inactive staff

### 📝 Attendance Management

* Record member attendance
* Track check-in information
* Track attendance status
* View attendance records
* Display today's attendance on the dashboard

### 💰 Expense Management

* Record gym expenses
* Track expense amounts
* Categorize/manage expense records
* Include expenses in financial calculations

### 🔔 Membership Reminders

* Identify memberships approaching expiry
* Display members whose memberships are expiring soon
* Help administrators follow up with members before expiry

### 🔐 Authentication & Security

* Admin authentication
* Password hashing
* JWT-based authentication
* Protected API functionality
* Role-based user structure

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* React Router
* Axios
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL
* Alembic
* JWT Authentication
* Uvicorn

### Testing & DevOps

* Pytest
* GitHub Actions
* PostgreSQL service in CI
* Automated Alembic migrations
* Automated backend test execution

## 🏗️ Project Architecture

```text
GYM/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── attendance.py
│   │   │       ├── auth.py
│   │   │       ├── dashboard.py
│   │   │       ├── expenses.py
│   │   │       ├── members.py
│   │   │       ├── membership_packages.py
│   │   │       ├── memberships.py
│   │   │       ├── payments.py
│   │   │       ├── reminders.py
│   │   │       ├── staff.py
│   │   │       └── trainers.py
│   │   │
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── scripts/
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── context/
    │   ├── layouts/
    │   ├── pages/
    │   ├── services/
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow that automatically validates the backend whenever code is pushed to or a pull request is opened against the `main` branch.

The pipeline:

1. Checks out the repository
2. Sets up Python 3.13
3. Starts a PostgreSQL 16 service
4. Installs backend dependencies
5. Runs Alembic database migrations
6. Executes the Pytest test suite

This helps ensure that changes do not break the application's backend functionality.

## 🧪 Testing

The backend includes automated tests covering important application functionality, including:

* Health checks
* Authentication
* Member management
* Memberships
* Payments
* Dashboard
* Attendance
* Trainers
* Staff
* Membership reminders

Run the tests with:

```bash
cd backend
pytest -v
```

## 🗄️ Database Migrations

The project uses **Alembic** for database schema management.

Apply the latest migrations:

```bash
cd backend
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

## ⚙️ Backend Setup

### 1. Clone the repository

```bash
git clone <https://github.com/Saimasad123/GYM-Managment-System>
cd GYM/backend
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `backend` directory.

Example:

```env
DATABASE_URL=postgresql+psycopg2://gym_user:gym_password@localhost:5432/gym_management
JWT_SECRET_KEY=your-secret-key
```

> Never commit real credentials, database passwords, or secret keys to GitHub.

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## 💻 Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## 🔌 API Modules

The backend API is organized under:

```text
/api/v1
```

Major API modules include:

```text
/api/v1/auth
/api/v1/members
/api/v1/membership-packages
/api/v1/memberships
/api/v1/payments
/api/v1/dashboard
/api/v1/attendance
/api/v1/trainers
/api/v1/expenses
/api/v1/staff
/api/v1/reminders
```

## 🩺 Health Checks

The application provides basic health endpoints:

```text
GET /
GET /health
GET /health/database
```

These endpoints can be used to verify that the API and database connection are functioning correctly.

## 📈 Financial Reporting

The system calculates financial performance using payment and expense records.

It provides:

```text
Revenue
Expenses
Profit
```

for:

* Daily performance
* Current month
* Current year

The dashboard also provides daily financial summaries that allow administrators to monitor revenue, expenses, and profit over time.

## 🔒 Security

Security-related functionality includes:

* Password hashing
* JWT authentication
* Protected API access
* Environment-based configuration
* Separation of configuration and application code

Sensitive configuration should always be stored in environment variables rather than committed to source control.

## 🎯 Project Goals

The main goal of this project was to build a practical, maintainable gym administration platform while applying real-world software engineering practices such as:

* REST API development
* Database design
* Authentication
* ORM-based data access
* Database migrations
* Automated testing
* Frontend/backend separation
* CI automation
* Modular application architecture

## 🚀 Future Improvements

Potential future improvements include:

* Role-based permissions for different staff types
* Member profile photos
* QR/barcode-based attendance
* Automated email/SMS membership reminders
* Online payment integration
* Advanced analytics
* Exportable financial reports
* Cloud deployment
* Docker containerization
* Production monitoring and logging

## 👨‍💻 Author

**Saim Asad**

Software Engineering Student | Full-Stack Developer

Built using **React, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pytest, and GitHub Actions**.

## 📄 License

This project is intended for educational and portfolio purposes.
