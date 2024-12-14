from sqlalchemy.orm import Session
from . import models
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(db: Session, username: str, email: str, password: str, role: models.UserRole):
    """Create a new user"""
    hashed_password = generate_password_hash(password)
    db_user = models.User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not check_password_hash(user.password, password):
        return None
    return user

def get_menu_items(db: Session, skip: int = 0, limit: int = 100):
    """Get all menu items"""
    return db.query(models.MenuItem).offset(skip).limit(limit).all()

def create_order(db: Session, customer_id: int, items: list):
    """Create a new order"""
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item in items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item["menu_item_id"]).first()
        if menu_item:
            subtotal = menu_item.price * item["quantity"]
            total_amount += subtotal
            order_items.append({
                "menu_item_id": item["menu_item_id"],
                "quantity": item["quantity"],
                "unit_price": menu_item.price,
                "subtotal": subtotal
            })
    
    # Create order
    db_order = models.Order(
        customer_id=customer_id,
        total_amount=total_amount,
        status=models.OrderStatus.PENDING
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item in order_items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            menu_item_id=item["menu_item_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=item["subtotal"]
        )
        db.add(db_order_item)
    
    db.commit()
    return db_order

def update_order_status(db: Session, order_id: int, status: models.OrderStatus):
    """Update order status"""
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get orders for a specific user"""
    return db.query(models.Order).filter(models.Order.customer_id == user_id).offset(skip).limit(limit).all()

def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    """Get all orders"""
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def update_user_password(db: Session, user_id: int, new_password: str):
    """Update user password"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.password = generate_password_hash(new_password)
        db.commit()
        db.refresh(user)
    return user
