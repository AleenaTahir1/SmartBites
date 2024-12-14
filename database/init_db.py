from database.config import engine
from database.models import Base
from database.seed_data import seed_database

def init_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Seed the database with initial data
    seed_database()

if __name__ == "__main__":
    init_database()
