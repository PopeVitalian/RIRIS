"""Konfiguracija, baza, predloge in skupne pomožne funkcije."""
import os
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Optional

from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

# ----------------------------------------------------------------
# Konfiguracija
# ----------------------------------------------------------------
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://avtotrg:avtotrg@localhost:5433/avtotrg_db",
)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
PER_PAGE = 25

FUELS = ("bencin", "dizel", "hibrid", "električni", "plin")
TRANSMISSIONS = ("ročni", "avtomatski")
USER_ROLES = ("buyer", "seller", "admin")
LISTING_STATUSES = ("aktivni", "rezerviran", "prodan", "blokiran")
OFFER_STATUSES = ("pending", "accepted", "rejected", "withdrawn")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# ----------------------------------------------------------------
# Poti
# ----------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# ----------------------------------------------------------------
# Baza
# ----------------------------------------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

class Base(DeclarativeBase):
    pass

def get_db():
    with Session(engine) as session:
        yield session

# ----------------------------------------------------------------
# Predloge
# ----------------------------------------------------------------
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))
templates.env.filters["eur"] = lambda v: f"{v:,.0f}".replace(",", ".") + " €"
templates.env.filters["km"] = lambda v: f"{v:,.0f}".replace(",", ".") + " km"

# ----------------------------------------------------------------
# Pomožne funkcije
# ----------------------------------------------------------------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def parse_int(raw) -> Optional[int]:
    try:
        return int(str(raw).strip())
    except (ValueError, TypeError):
        return None

def parse_money(raw) -> Optional[Decimal]:
    """Sprejme '12990', '12990,00' ali '12.990,50'."""
    cleaned = str(raw).replace("€", "").replace(" ", "").strip()
    if "," in cleaned and "." in cleaned:
        cleaned = (
            cleaned.replace(".", "").replace(",", ".")
            if cleaned.rfind(",") > cleaned.rfind(".")
            else cleaned.replace(",", "")
        )
    elif "," in cleaned:
        head, _, tail = cleaned.partition(",")
        cleaned = f"{head}.{tail}" if len(tail) == 2 else head + tail
    try:
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None

def valid_listing_form(fields: dict) -> Optional[str]:
    if not fields["make"] or not fields["model"]:
        return "Znamka in model sta obvezna."
    year_i = parse_int(fields["year"])
    if year_i is None or not 1950 <= year_i <= now_utc().year + 1:
        return f"Letnik mora biti med 1950 in {now_utc().year + 1}."
    mileage_i = parse_int(fields["mileage_km"])
    if mileage_i is None or mileage_i < 0:
        return "Prevoženi kilometri morajo biti nenegativno število."
    if fields["fuel"] not in FUELS:
        return "Neveljavno gorivo."
    if fields["transmission"] not in TRANSMISSIONS:
        return "Neveljaven menjalnik."
    price = parse_money(fields["price_eur"])
    if price is None or price <= 0:
        return "Cena mora biti pozitivno število."
    return None
