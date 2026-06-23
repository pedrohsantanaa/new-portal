from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    codename = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Permission {self.codename}>"


class UserPermission(Base):
    __tablename__ = "user_permissions"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id = Column(
        Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )
