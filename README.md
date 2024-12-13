# SmartBites: Smart Ordering for Cafeteria Meals

A modern, efficient meal ordering system for university cafeterias built with Python and PostgreSQL.

## 🚀 Features

### For Users
- **Account Management**
  - University credential-based authentication
  - Guest ordering capability
- **Interactive Menu**
  - Categorized food items
  - Detailed item descriptions with images
  - Real-time pricing
- **Order Management**
  - Shopping cart functionality
  - Customization options
  - Special request handling
- **Order Tracking**
  - Real-time status updates
  - Push notifications
  - Order history

### For Administrators
- **Secure Dashboard**
  - Real-time order monitoring
  - Order status management
- **Menu Management**
  - Add/Edit/Remove menu items
  - Price updates
  - Category management
- **Optional Analytics**
  - Popular items tracking
  - Peak hours analysis
  - Sales reporting

## 🛠️ Technology Stack

- **Frontend:** CustomTkinter (Modern GUI framework)
- **Backend:** Python 3.11+
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Additional Libraries:**
  - psycopg2 (PostgreSQL adapter)
  - plyer (notifications)
  - Pillow (image handling)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SmartBites.git
cd SmartBites
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
- Install PostgreSQL
- Create a database named 'smartbites'
- Update database configuration in config.py

5. Run the application:
```bash
python main.py
```

## 📊 Database Schema

### Users
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);
```

### Menu
```sql
CREATE TABLE menu (
    item_id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(255)
);
```

### Orders
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    status VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Order Items
```sql
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    item_id INTEGER REFERENCES menu(item_id),
    quantity INTEGER NOT NULL,
    special_requests TEXT
);
```

## 🔐 Environment Variables

Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_NAME=smartbites
DB_USER=your_username
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
