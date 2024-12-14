from database.config import SessionLocal
from database.models import User, MenuItem, UserRole
from database.utils import create_user
import os

def seed_database():
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # Create admin user
            admin = create_user(
                db=db,
                username="admin",
                email="admin@smartbites.com",
                password="admin123",
                role=UserRole.ADMIN
            )

        # Check if staff user exists
        staff = db.query(User).filter(User.username == "staff").first()
        if not staff:
            # Create staff user
            staff = create_user(
                db=db,
                username="staff",
                email="staff@smartbites.com",
                password="staff123",
                role=UserRole.STAFF
            )

        # Check if test customer exists
        customer = db.query(User).filter(User.username == "customer").first()
        if not customer:
            # Create test customer
            customer = create_user(
                db=db,
                username="customer",
                email="customer@example.com",
                password="customer123",
                role=UserRole.CUSTOMER
            )

        # Check if menu items exist
        menu_items_count = db.query(MenuItem).count()
        if menu_items_count == 0:
            # Create menu items
            menu_items = [
                {
                    "name": "Chicken Biryani",
                    "description": "Aromatic basmati rice cooked with tender chicken and spices",
                    "price": 350.00,
                    "category": "Main Course",
                    "image_path": os.path.join("assets", "food", "biryani.png"),
                    "available": 1
                },
                {
                    "name": "Beef Burger",
                    "description": "Juicy beef patty with fresh vegetables and special sauce",
                    "price": 250.00,
                    "category": "Fast Food",
                    "image_path": os.path.join("assets", "food", "burger.png"),
                    "available": 1
                },
                {
                    "name": "Chicken Macaroni",
                    "description": "Creamy macaroni pasta with chicken and white sauce",
                    "price": 200.00,
                    "category": "Pasta",
                    "image_path": os.path.join("assets", "food", "macaroni.png"),
                    "available": 1
                },
                {
                    "name": "Chicken Qorma",
                    "description": "Traditional Pakistani curry with tender chicken",
                    "price": 300.00,
                    "category": "Main Course",
                    "image_path": os.path.join("assets", "food", "qorma.png"),
                    "available": 1
                },
                {
                    "name": "Chicken Roll",
                    "description": "Spicy chicken wrapped in fresh paratha",
                    "price": 150.00,
                    "category": "Snacks",
                    "image_path": os.path.join("assets", "food", "rolls.png"),
                    "available": 1
                },
                {
                    "name": "Vegetable Samosa",
                    "description": "Crispy pastry filled with spiced potatoes and peas",
                    "price": 50.00,
                    "category": "Snacks",
                    "image_path": os.path.join("assets", "food", "samosa.png"),
                    "available": 1
                }
            ]

            # Add menu items to database
            for item_data in menu_items:
                menu_item = MenuItem(**item_data)
                db.add(menu_item)

            db.commit()
            print("Menu items added successfully!")
        
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
