from app.db.session import SessionLocal
from app.db.models import User, Product
from app.core.security import get_password_hash


def seed_db():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@example.com").first():
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("Admin123!"),
                is_active=True,
            )
            db.add(admin)

        if db.query(Product).count() == 0:
            products = [
                Product(title="Wireless Mouse", description="Ergonomic optical mouse", price=29.99, stock=50),
                Product(title="Mechanical Keyboard", description="RGB gaming keyboard", price=89.99, stock=30),
                Product(title="4K Monitor", description="27-inch IPS display", price=349.99, stock=15),
            ]
            db.add_all(products)

        db.commit()
        print("Successfully seeded initial database records!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
