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
- **Search Books**  
  - Can only **view** and **search** books  
  - Cannot add, issue, or return books
- **My Transactions**  
  - Can only **view their own transactions**  
  - Cannot return books (Admin only)
- Request to issue a book
- Pay fines via mock-payment
- View personal membership details

---

## 📂 Project Structure
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

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Initialize Database
python init_db.py

This creates library.db with seeded:
Admin user → admin@example.com / Admin@123
Sample Books, Movies, Memberships

5️⃣ Run the Application
python -m app.main

🔐 Default Login Credentials
Admin
Email: admin@example.com
Password: Admin@123
User
Create new users from the User Management section (Admin only)

📊 Database Schema
Key tables include:
users → Admins & Users
books → Library books
movies → Library movies
memberships → Membership types
issues → Book issue records
transactions → Payments & fines
logs → Audit trail

🧾 Requirements
Dependencies are listed in requirements.txt:
bcrypt==4.1.2
pytest==8.3.3      # optional (for testing)
pyinstaller==6.10.0 # optional (for packaging)
Install with:
pip install -r requirements.txt

🧪 Testing
Basic test cases can be added with unittest or pytest.
Example:
pytest tests/

🚀 Deployment
This project is desktop-based, but can be bundled into an executable using PyInstaller:
pyinstaller --onefile --noconsole app/main.py

📌 Notes
Admin-only actions are hidden from users (e.g., Add/Issue/Return).
Users can search books and view only their own transactions.
Fine calculation default: ₹2 per day overdue (configurable in code).
All assumptions and unspecified behaviors are documented in ASSUMPTIONS.md.

📝 License
This project is open-source under the MIT License.
Feel free to use, modify, and distribute.

💡 Future Improvements
Export reports in PDF/Excel format
Add search filters and sorting
Improve UI/UX styling
Add test coverage for all modules

