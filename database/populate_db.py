from .config import SessionLocal
from .models import User, MenuItem, Order, OrderItem, UserRole, OrderStatus
from .utils import create_user
from datetime import datetime, timedelta
import random

def populate_database():
    db = SessionLocal()
    
    # Create users
    users = [
        ("admin", "admin@smartbites.com", "admin123", UserRole.ADMIN),
        ("staff1", "staff1@smartbites.com", "staff123", UserRole.STAFF),
        ("john_doe", "john@example.com", "john123", UserRole.CUSTOMER),
        ("jane_smith", "jane@example.com", "jane123", UserRole.CUSTOMER),
        ("mike_wilson", "mike@example.com", "mike123", UserRole.CUSTOMER)
    ]
    
    created_users = []
    for username, email, password, role in users:
        try:
            user = create_user(db, username, email, password, role)
            created_users.append(user)
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error creating user {username}: {e}")
    
    # Create menu items
    menu_items = [
        ("Classic Burger", "Juicy beef patty with fresh lettuce, tomato, and special sauce", 8.99, "Burgers", "burger.jpg"),
        ("Chicken Wings", "Crispy wings with choice of sauce", 10.99, "Appetizers", "wings.jpg"),
        ("Caesar Salad", "Fresh romaine lettuce with parmesan and croutons", 7.99, "Salads", "caesar.jpg"),
        ("Margherita Pizza", "Fresh mozzarella, tomatoes, and basil", 12.99, "Pizza", "pizza.jpg"),
        ("Chocolate Brownie", "Warm chocolate brownie with vanilla ice cream", 5.99, "Desserts", "brownie.jpg"),
        ("French Fries", "Crispy golden fries with seasoning", 3.99, "Sides", "fries.jpg"),
        ("Veggie Wrap", "Fresh vegetables with hummus in a tortilla wrap", 7.99, "Wraps", "wrap.jpg"),
        ("Soda", "Choice of soft drinks", 1.99, "Beverages", "soda.jpg")
    ]
    
    created_menu_items = []
    for name, desc, price, category, image in menu_items:
        menu_item = MenuItem(
            name=name,
            description=desc,
            price=price,
            category=category,
            image_path=image,
            available=1
        )
        db.add(menu_item)
        created_menu_items.append(menu_item)
    
    db.commit()
    print("Created menu items")
    
    # Create orders
    statuses = [OrderStatus.PENDING, OrderStatus.PROCESSING, OrderStatus.COMPLETED]
    
    # Create orders for the last 7 days
    for i in range(20):
        # Random customer
        customer = random.choice([u for u in created_users if u.role == UserRole.CUSTOMER])
        
        # Random order items (1-4 items per order)
        num_items = random.randint(1, 4)
        order_items = random.sample(created_menu_items, num_items)
        
        # Calculate total
        total_amount = 0
        for item in order_items:
            total_amount += item.price * random.randint(1, 3)
        
        # Random date within last 7 days
        days_ago = random.randint(0, 7)
        order_date = datetime.utcnow() - timedelta(days=days_ago)
        
        # Create order
        order = Order(
            customer_id=customer.id,
            status=random.choice(statuses),
            total_amount=total_amount,
            created_at=order_date,
            updated_at=order_date
        )
        db.add(order)
        db.commit()
        
        # Create order items
        for item in order_items:
            quantity = random.randint(1, 3)
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item.id,
                quantity=quantity,
                unit_price=item.price,
                subtotal=item.price * quantity
            )
            db.add(order_item)
        
        print(f"Created order {order.id} for customer {customer.username}")
    
    db.commit()
    db.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    populate_database()
