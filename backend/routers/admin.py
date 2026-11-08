"""Adminove poti: uporabniki, oglasi, blokade, vloge."""
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..auth import ctx, flash, require_role
from ..models import Listing, Offer, User
from ..settings import USER_ROLES, get_db, now_utc, templates

router = APIRouter(prefix="/admin")

@router.get("/dashboard")
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    stats = {
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "listings": db.scalar(select(func.count()).select_from(Listing)) or 0,
        "offers": db.scalar(select(func.count()).select_from(Offer)) or 0,
    }
    return templates.TemplateResponse(
        request, "admin_dashboard.html", {**ctx(request, db), "stats": stats}
    )

@router.get("/users")
def admin_users(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
    q: str = Query("", max_length=60),
):
    stmt = select(User).order_by(User.created_at.desc())
    if q:
        stmt = stmt.where(User.email.ilike(f"%{q}%"))
    users = db.scalars(stmt).all()
    return templates.TemplateResponse(
        request, "admin_users.html", {**ctx(request, db), "users": users, "q": q}
    )

@router.get("/listings")
def admin_listings(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
    q: str = Query("", max_length=60),
):
    stmt = select(Listing).order_by(Listing.created_at.desc())
    if q:
        stmt = stmt.where(or_(Listing.make.ilike(f"%{q}%"), Listing.model.ilike(f"%{q}%")))
    listings = db.scalars(stmt).all()
    return templates.TemplateResponse(
        request, "admin_listings.html", {**ctx(request, db), "listings": listings, "q": q}
    )

@router.post("/users/{user_id}/block")
async def admin_block_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    u = db.get(User, user_id)
    if u is None:
        raise HTTPException(404, "Uporabnik ne obstaja.")
    if u.id == admin.id:
        flash(request, "Ne morete blokirati samega sebe.", "error")
        return RedirectResponse("/admin/users", status_code=303)
    if u.role == "admin":
        flash(request, "Drugega administratorja ni mogoče blokirati.", "error")
        return RedirectResponse("/admin/users", status_code=303)
    u.is_blocked = True
    db.commit()
    flash(request, f"Uporabnik {u.email} blokiran.", "success")
    return RedirectResponse("/admin/users", status_code=303)

@router.post("/users/{user_id}/unblock")
async def admin_unblock_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    u = db.get(User, user_id)
    if u is None:
        raise HTTPException(404, "Uporabnik ne obstaja.")
    u.is_blocked = False
    db.commit()
    flash(request, f"Uporabnik {u.email} odblokiran.", "success")
    return RedirectResponse("/admin/users", status_code=303)

@router.post("/users/{user_id}/role")
async def admin_change_role(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
    new_role: str = Form(""),
):
    u = db.get(User, user_id)
    if u is None:
        raise HTTPException(404, "Uporabnik ne obstaja.")
    if u.id == admin.id:
        flash(request, "Svoje vloge ne morete spremeniti.", "error")
        return RedirectResponse("/admin/users", status_code=303)
    if new_role not in USER_ROLES:
        flash(request, "Neveljavna vloga.", "error")
        return RedirectResponse("/admin/users", status_code=303)
    u.role = new_role
    db.commit()
    flash(request, f"Vloga uporabnika {u.email} spremenjena v {new_role}.", "success")
    return RedirectResponse("/admin/users", status_code=303)

@router.post("/listings/{listing_id}/block")
async def admin_block_listing(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Oglas ne obstaja.")
    listing.status = "blokiran"
    listing.updated_at = now_utc()
    db.commit()
    flash(request, "Oglas blokiran.", "success")
    return RedirectResponse("/admin/listings", status_code=303)

@router.post("/listings/{listing_id}/delete")
async def admin_delete_listing(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Oglas ne obstaja.")
    db.delete(listing)
    db.commit()
    flash(request, "Oglas izbrisan.", "success")
    return RedirectResponse("/admin/listings", status_code=303)
