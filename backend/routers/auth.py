"""Registracija, prijava in odjava."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..auth import ctx, flash, get_current_user
from ..models import User, hash_password
from ..settings import EMAIL_RE, get_db, now_utc

router = APIRouter(prefix="/auth")

@router.get("/register")
def register_form(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse("/", status_code=303)
    return templates_response(request, "auth_register.html", ctx(request, db))

@router.post("/register")
async def register(
    request: Request,
    db: Session = Depends(get_db),
    full_name: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
    password_confirm: str = Form(""),
    city: str = Form(""),
    role: str = Form("buyer"),
    is_dealer: str = Form(""),
):
    def back(msg: str):
        flash(request, msg, "error")
        return RedirectResponse("/auth/register", status_code=303)

    full_name = full_name.strip()
    email_s = email.strip().lower()
    city = city.strip()

    if not full_name or not email_s or not password or not city:
        return back("Vsa polja so obvezna.")
    if not EMAIL_RE.match(email_s):
        return back("Vpiši veljaven e-poštni naslov.")
    if len(password) < 8:
        return back("Geslo mora imeti vsaj 8 znakov.")
    if password != password_confirm:
        return back("Gesli se ne ujemata.")
    if role not in ("buyer", "seller"):
        return back("Neveljavna vloga.")
    if db.scalar(select(User).where(User.email == email_s)):
        return back("Račun s to e-pošto že obstaja.")

    user = User(
        email=email_s,
        password_hash=hash_password(password),
        full_name=full_name,
        city=city,
        role=role,
        is_dealer=(is_dealer == "1" and role == "seller"),
        is_blocked=False,
        created_at=now_utc(),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return back("Račun s to e-pošto že obstaja.")

    flash(request, "Registracija uspešna. Zdaj se lahko prijavite.", "success")
    return RedirectResponse("/auth/login", status_code=303)

@router.get("/login")
def login_form(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse("/", status_code=303)
    return templates_response(request, "auth_login.html", ctx(request, db))

@router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(""),
    password: str = Form(""),
):
    email_s = email.strip().lower()
    user = db.scalar(select(User).where(User.email == email_s))
    if not user or not user.check_password(password):
        flash(request, "Napačna e-pošta ali geslo.", "error")
        return RedirectResponse("/auth/login", status_code=303)
    if user.is_blocked:
        flash(request, "Vaš račun je blokiran. Obrnite se na administratorja.", "error")
        return RedirectResponse("/auth/login", status_code=303)
    request.session["user_id"] = user.id
    flash(request, f"Dobrodošli, {user.full_name}.", "success")
    return RedirectResponse("/", status_code=303)

@router.post("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    flash(request, "Odjavljeni ste.", "success")
    return RedirectResponse("/listings", status_code=303)

def templates_response(request, name, context):
    from ..settings import templates

    return templates.TemplateResponse(request, name, context)
