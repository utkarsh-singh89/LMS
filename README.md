# 📚 Library Management System (Python + Tkinter + SQLite)

A complete **Library Management System** built using **Python**, **Tkinter** (for GUI), and **SQLite** (as backend database).  
This project provides role-based access for **Admin** and **Users**, following business rules similar to real-world library systems.

---

## ✨ Features

### 🔑 Authentication
- Login for **Admin** and **User**
- Passwords stored securely (hashed with `bcrypt`)
- Role-based navigation

### 👩‍💼 Admin Features
- Manage **Books** (Add, Issue, Return, Delete, Update)
- Manage **Movies**
- Manage **Memberships**
- Manage **Users** (Add/Edit/Delete)
- Approve/Deny **Issue Requests**
- View **Reports** and **Transactions**
- Perform **Maintenance Tasks** (import/export, data reset)

### 👤 User Features
- **Search Books** (view-only — cannot add, issue, or return)
- **My Transactions** (view personal transactions only, cannot return)
- Request to issue a book
- Pay fines via mock-payment
- View personal membership details

---

LMS/
│
├── app/
│ ├── main.py # Application entry point
│ ├── models.py # Database models and queries
│ ├── auth.py # Authentication logic
│ ├── book_management.py # Book management GUI
│ ├── transactions.py # Transactions & issues GUI
│ ├── user_management.py # User management (admin only)
│ ├── membership.py # Membership management
│ ├── movie_management.py # Movie management
│ ├── maintenance.py # Maintenance & import tools
│ └── ...
│
├── init_db.py # Initialize and seed SQLite DB
├── requirements.txt # Python dependencies
├── ASSUMPTIONS.md # Documented assumptions
└── README.md # Project documentation


---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/utkarsh-singh89/LMS.git
cd LMS

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

python init_db.py

This creates library.db with seeded:

Admin user → admin@example.com / Admin@123

Sample Books, Movies, Memberships
python -m app.main

Default Login Credentials

Admin

Email: admin@example.com

Password: Admin@123

User

Create new users from the User Management section (Admin only)

## 📂 Project Structure

