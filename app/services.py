from typing import Optional, List, Union
from sqlalchemy.orm import Session
from app.db_models import UserDB, ProductDB
from app.auth import hash_password, verify_password
from app.models import UserCreate, Product, Order

# ---------------- USER SERVICES ----------------

def register_user_service(db: Session, user: UserCreate) -> Optional[UserDB]:
    """
    Registers a new user.
    Returns the UserDB object if successful, None if username exists.
    """
    existing: Optional[UserDB] = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing:
        return None

    new_user = UserDB(
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user_service(db: Session, user: UserCreate) -> Optional[UserDB]:
    """
    Checks user credentials.
    Returns UserDB object if successful, None if invalid.
    """
    db_user: Optional[UserDB] = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user:
        return None

    if not verify_password(user.password, db_user.password):
        return None

    return db_user


# ---------- PRODUCT SERVICES ----------

def add_multiple_products_service(db: Session, products: List[Product]) -> dict:
    from sqlalchemy.exc import IntegrityError
    try:
        for product in products:
            existing = db.query(ProductDB).filter(ProductDB.product_id == product.product_id).first()
            if existing:
                continue  # skip duplicates
            db.add(ProductDB(**product.dict()))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    return {"message": "Products added successfully"}

def get_all_products_service(db: Session) -> List[ProductDB]:
    return db.query(ProductDB).all()

def delete_product_service(db: Session, product_id: str) -> Optional[bool]:
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return True

def update_product_stock_service(db: Session, product_id: str, quantity: int) -> Optional[ProductDB]:
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        return None
    product.quantity += quantity
    db.commit()
    db.refresh(product)
    return product

def search_product_service(db: Session, name: str) -> List[ProductDB]:
    return db.query(ProductDB).filter(ProductDB.name.ilike(f"%{name}%")).all()

def create_order_service(db: Session, product_id: str, quantity: int) -> Union[str, ProductDB]:
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        return "not_found"
    if product.quantity < quantity:
        return "insufficient_stock"
    product.quantity -= quantity
    db.commit()
    db.refresh(product)
    return product