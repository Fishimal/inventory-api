from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine, Base
from app.models import UserCreate, UserResponse, ProductList, ProductResponse
from app.services import (
    register_user_service,
    login_user_service,
    add_multiple_products_service,
    get_all_products_service,
    update_product_stock_service,
    delete_product_service,
    search_product_service,
    create_order_service
)
from app.auth import create_access_token, get_current_user, require_admin

# ---------- CREATE TABLES ----------
Base.metadata.create_all(bind=engine)

# ---------- APP ----------
app = FastAPI(title="Inventory API with RBAC")

# ---------- DB DEPENDENCY ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- ROOT PAGE ----------
@app.get("/")
def root():
    return {"message": "Inventory API is running 🚀"}


# ---------- FIRST ADMIN CREATION (ON STARTUP) ----------
@app.on_event("startup")
def create_first_admin():
    db = SessionLocal()
    from app.db_models import UserDB

    admin_exists = db.query(UserDB).filter(UserDB.role == "admin").first()
    if not admin_exists:
        # Replace these credentials or use environment variables
        first_admin = UserCreate(username="admin", password="AdminPass123", role="admin")
        register_user_service(db, first_admin)
        print("✅ First admin created: username=admin, password=AdminPass123")
    db.close()


# ---------- REGISTER USER (ADMIN-CONTROLLED) ----------
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # must be logged in
):
    # Only admins can create another admin
    if user.role == "admin" and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create another admin")

    # Force role to 'user' if not admin
    if user.role != "admin":
        user.role = "user"

    new_user = register_user_service(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    return new_user


# ---------- PUBLIC SELF-REGISTRATION (USER ONLY) ----------
@app.post("/register-public", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_public(user: UserCreate, db: Session = Depends(get_db)):
    # Force role to 'user' always
    user.role = "user"
    new_user = register_user_service(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return new_user


# ---------- LOGIN ----------
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Temporary object to validate credentials
    user = UserCreate(username=form_data.username, password=form_data.password)
    db_user = login_user_service(db, user)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Include role in JWT for RBAC
    token = create_access_token({
        "sub": db_user.username,
        "role": db_user.role
    })

    return {"access_token": token, "token_type": "bearer"}


# ---------- PRODUCT ROUTES (EXAMPLE RBAC) ----------

@app.post("/products/bulk")
def add_multiple_products(
    product_list: ProductList,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)  # Admin-only
):
    return add_multiple_products_service(db, product_list.products)


@app.put("/products/{product_id}/stock")
def update_stock(
    product_id: str,
    quantity: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)  # Admin-only
):
    result = update_product_stock_service(db, product_id, quantity)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Stock updated"}


@app.delete("/products/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)  # Admin-only
):
    result = delete_product_service(db, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted"}


# ---------- PRODUCTS VIEW (USER & ADMIN) ----------
@app.get("/products", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # any logged-in user
):
    return get_all_products_service(db)


@app.get("/products/search/{name}", response_model=List[ProductResponse])
def search_product(
    name: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return search_product_service(db, name)


# ---------- ORDERS (USER & ADMIN) ----------
@app.post("/orders")
def create_order(
    order: ProductList,  # replace with your Order schema
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    from app.models import Order
    for o in order.products:
        result = create_order_service(db, o.product_id, o.quantity)
        if result == "not_found":
            raise HTTPException(status_code=404, detail=f"Product {o.product_id} not found")
        if result == "insufficient_stock":
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {o.product_id}")
    return {"message": "Order placed"}