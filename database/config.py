from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to default database
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="annie",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create a cursor object
    cur = conn.cursor()
    
    # Check if database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'smartbites'")
    exists = cur.fetchone()
    
    if not exists:
        # Create the database
        cur.execute('CREATE DATABASE smartbites')
        print("Database 'smartbites' created successfully!")
    
    # Close the cursor and connection
    cur.close()
    conn.close()

# Create database if it doesn't exist
create_database()

# Database connection settings
DATABASE_URL = "postgresql://postgres:annie@localhost:5432/smartbites"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
