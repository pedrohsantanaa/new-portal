import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.utils.auth import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@fomento.to.gov.br").first()
        if admin:
            print("Admin já existe.")
            return
        admin = User(
            email="admin@fomento.to.gov.br",
            hashed_password=hash_password("admin123"),
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print("Admin criado com sucesso!")
        print("  Email: admin@fomento.to.gov.br")
        print("  Senha: admin123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
