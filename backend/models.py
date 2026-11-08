"""SQLAlchemy modeli: User, Listing, Offer."""
from datetime import datetime
from decimal import Decimal
from typing import Optional

import bcrypt
from sqlalchemy import (
    BigInteger,
    Boolean,
    Enum as SaEnum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .settings import (
    Base,
    FUELS,
    LISTING_STATUSES,
    OFFER_STATUSES,
    TRANSMISSIONS,
    USER_ROLES,
)

# ----------------------------------------------------------------
# Gesla
# ----------------------------------------------------------------
def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(pw: str, h: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode("utf-8"), h.encode("utf-8"))
    except (ValueError, TypeError):
        return False

# ----------------------------------------------------------------
# Modeli
# ----------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[str] = mapped_column(
        SaEnum(*USER_ROLES, name="user_role", create_type=False),
        nullable=False,
        default="buyer",
    )
    is_dealer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)