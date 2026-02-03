from core.database import SessionLocal, engine, Base
from core.models import Product, User, Order
from datetime import datetime, timedelta
import random


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if db.query(Product).count() > 0:
        print("Database already contains data. Skipping seed.")
        db.close()
        return

    print("Seeding database with large dataset...")

    categories = ["Electronics", "Audio", "Gaming", "Accessories", "Furniture", "Software"]
    product_types = [
        "Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse",
        "Headphones", "Speaker", "Microphone", "Camera", "Drone", "Watch",
        "Console", "Controller", "VR Headset", "Chair", "Desk", "Light"
    ]
    brands = ["Dell", "Apple", "Samsung", "Sony", "Logitech", "Razer", "Corsair", "ASUS", "HP", "Lenovo"]

    print("Generating 1000 products...")
    products = []
    for i in range(1000):
        brand = random.choice(brands)
        product_type = random.choice(product_types)

        products.append(Product(
            name=f"{brand} {product_type} {random.choice(['Pro', 'Max', 'Ultra', 'Plus', 'Elite', ''])} {i}",
            price=random.randint(2900, 999900),
            category=random.choice(categories),
            stock=random.randint(0, 150),
            created_at=datetime.now() - timedelta(days=random.randint(1, 730))
        ))

    db.add_all(products)
    db.commit()
    print(f"Added {len(products)} products")

    first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava", "Robert", "Isabella",
                   "David", "Mia", "Richard", "Charlotte", "Joseph", "Amelia", "Thomas", "Harper", "Charles", "Evelyn"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                  "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
                  "Martin"]
    countries = ["USA", "Canada", "UK", "Germany", "France", "Spain", "Italy", "Poland", "Australia", "Japan",
                 "Netherlands", "Sweden", "Norway", "Denmark", "Belgium", "Switzerland", "Austria", "Ireland"]

    print("Generating 500 users...")
    users = []
    for i in range(500):
        first = random.choice(first_names)
        last = random.choice(last_names)
        username = f"{first.lower()}.{last.lower()}{i}"
        email = f"{username}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com'])}"

        users.append(User(
            username=username,
            email=email,
            country=random.choice(countries),
            created_at=datetime.now() - timedelta(days=random.randint(1, 1095))
        ))

    db.add_all(users)
    db.commit()
    print(f"Added {len(users)} users")

    print("Generating 5000 orders...")
    orders = []
    for i in range(5000):
        user = random.choice(users)
        product = random.choice(products)
        quantity = random.randint(1, 10)

        orders.append(Order(
            user_id=user.id,
            product_id=product.id,
            quantity=quantity,
            total_price=product.price * quantity,
            created_at=datetime.now() - timedelta(days=random.randint(1, 365))
        ))

        if (i + 1) % 1000 == 0:
            db.add_all(orders)
            db.commit()
            orders = []
            print(f"  Progress: {i + 1}/5000 orders")

    if orders:
        db.add_all(orders)
        db.commit()

    print(f"Added 5000 orders")
    print("Database seeding complete!")

    db.close()


if __name__ == "__main__":
    seed_database()