"""Pomožne funkcije za sejo, prijavo in preverjanje vlog."""
from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .models import User
from .settings import engine, get_db

def flash(request: Request, message: str, category: str = "success") -> None:
    request.session["_flash"] = {"message": message, "category": category}

def get_current_user(request: Request, db: Session) -> Optional[User]:
    uid = request.session.get("user_id")
    if not uid:
        return None
    user = db.get(User, uid)
    if user is None or user.is_blocked:
        request.session.pop("user_id", None)
        return None
    return user

def ctx(request: Request, db: Session, **extra) -> dict:
    msg = request.session.pop("_flash", None)
    return {
        "request": request,
        "user": get_current_user(request, db),
        "messages": [msg] if msg else [],
        **extra,
    }

def require_role(*roles: str):
    """FastAPI dependency: preveri prijavo in vlogo."""

    def dep(request: Request, db: Session = Depends(get_db)) -> User:
        user = get_current_user(request, db)
        if user is None:
            raise HTTPException(401, "Prijava je obvezna.")
        if roles and user.role not in roles:
            raise HTTPException(403, "Dostop zavrnjen.")
        return user

    return dep

def safe_user(request: Request) -> Optional[User]:
    """Uporabnik za prikaz v predlogi – ne sproži izjem."""
    try:
        uid = request.session.get("user_id")
        if not uid:
            return None
        from sqlalchemy.orm import Session as ORMSession

        with ORMSession(engine) as s:
            return s.get(User, uid)
    except Exception:
        return None
