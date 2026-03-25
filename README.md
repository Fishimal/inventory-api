# 🧾 Inventory Management System API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A **production-style backend system** built using FastAPI to manage products, inventory, and orders with secure JWT-based authentication and role-based access control.

---

## 🌍 Live Demo

* API Base URL: https://inventory-api-camq.onrender.com
* Swagger Docs: https://inventory-api-camq.onrender.com/docs

---

## 🚀 Features

* 🔐 JWT Authentication (Login/Register)
* 👑 Role-Based Access Control (Admin/User)
* 📦 Product Management (Admin only)
* 🛒 Order Processing with stock validation
* 🔍 Product Search (case-insensitive)
* 🔒 Protected routes using OAuth2 & Bearer tokens
* 💾 SQLite Database with SQLAlchemy ORM
* 🧠 Clean architecture (routes → services → DB)

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Language:** Python 3.12
* **Database:** SQLite (SQLAlchemy ORM)
* **Authentication:** JWT (`python-jose`)
* **Security:** Passlib (`bcrypt`)

---

## 📂 Project Structure

```
inventory_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py        # API routes
│   ├── database.py    # DB connection
│   ├── db_models.py   # SQLAlchemy models
│   ├── models.py      # Pydantic schemas
│   ├── services.py    # Business logic
│   └── auth.py        # JWT + RBAC
│
├── inventory_api_venv/
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Fishimal/inventory-api.git
cd inventory-api
```

---

### 2. Create virtual environment

```bash
python -m venv inventory_api_venv

# Mac/Linux
source inventory_api_venv/bin/activate  

# Windows
inventory_api_venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

---

## 🌐 API Documentation

Once the server is running:

👉 http://127.0.0.1:8000/docs

Interactive Swagger UI for testing all endpoints.

---

## 🔐 Authentication Flow

1. Register a user → `/register-public`
2. Login → `/login`
3. Copy the access token
4. Click **Authorize 🔒** in Swagger
5. Enter:

```
Bearer <your_token>
```

---

## 👑 Default Admin

On first startup, a default admin is created:

* **Username:** `admin`
* **Password:** `AdminPass123`

Use this account to create other admins.

---

## 📌 API Endpoints

### 🔐 Auth

| Method | Endpoint         | Description                      |
| ------ | ---------------- | -------------------------------- |
| POST   | /register        | Register user (admin-controlled) |
| POST   | /register-public | Public user registration         |
| POST   | /login           | Login & get JWT token            |

---

### 📦 Products

| Method | Endpoint                     | Access | Description           |
| ------ | ---------------------------- | ------ | --------------------- |
| POST   | /products/bulk               | Admin  | Add multiple products |
| GET    | /products                    | All    | Get all products      |
| PUT    | /products/{product_id}/stock | Admin  | Update stock          |
| DELETE | /products/{product_id}       | Admin  | Delete product        |
| GET    | /products/search/{name}      | All    | Search products       |

---

### 🛒 Orders

| Method | Endpoint | Access | Description  |
| ------ | -------- | ------ | ------------ |
| POST   | /orders  | All    | Create order |

---

## 📥 Sample Request

### Add Products (Admin only)

```json
{
  "products": [
    {
      "product_id": "P001",
      "name": "Laptop",
      "quantity": 10,
      "price": 500
    }
  ]
}
```

---

## 🧪 Example Use Case

* Add products to inventory
* Search products by name
* Update stock when new items arrive
* Place orders and automatically reduce stock
* Prevent orders if stock is insufficient

---

## 🚀 Future Enhancements

* 🔁 Refresh Tokens & Token Revocation
* 🐘 PostgreSQL (Production DB)
* 🐳 Docker Containerization
* 📊 Admin Dashboard (React)
* ⚡ Redis Caching
* 📜 Logging & Monitoring

---

## 👩‍💻 Author

**Rubina Das**

---

## ⭐ Notes

* Follows modular backend architecture
* Designed for real-world API development
* Suitable for backend developer roles & interviews
