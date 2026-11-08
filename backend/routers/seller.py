"""Prodajalčeve poti: upravljanje oglasov."""
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..auth import ctx, flash, require_role
from ..models import Listing, User
from ..settings import (
    FUELS,
    TRANSMISSIONS,
    get_db,
    now_utc,
    parse_money,
    templates,
    valid_listing_form,
)

router = APIRouter(prefix="/seller")

@router.get("/listings")
def seller_listings(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    listings = db.scalars(
        select(Listing).where(Listing.seller_id == user.id)
        .order_by(Listing.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        request, "seller_listings.html", {**ctx(request, db), "listings": listings}
    )

def _listing_form_ctx(request, db, listing=None, form_action="/seller/listings/new"):
    return {
        **ctx(request, db),
        "listing": listing,
        "form_action": form_action,
        "fuels": FUELS,
        "transmissions": TRANSMISSIONS,
    }

@router.get("/listings/new")
def seller_listing_new_form(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    return templates.TemplateResponse(
        request, "seller_listing_form.html", _listing_form_ctx(request, db)
    )

@router.post("/listings/new")
async def seller_listing_new(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
    make: str = Form(""),
    model: str = Form(""),
    year: str = Form(""),
    mileage_km: str = Form(""),
    fuel: str = Form(""),
    transmission: str = Form(""),
    price_eur: str = Form(""),
    description: str = Form(""),
):
    fields = {
        "make": make.strip(), "model": model.strip(), "year": year,
        "mileage_km": mileage_km, "fuel": fuel, "transmission": transmission,
        "price_eur": price_eur,
    }
    error = valid_listing_form(fields)
    if error:
        flash(request, error, "error")
        return RedirectResponse("/seller/listings/new", status_code=303)

    listing = Listing(
        seller_id=user.id,
        make=fields["make"], model=fields["model"],
        year=int(year), mileage_km=int(mileage_km),
        fuel=fuel, transmission=transmission,
        price_eur=parse_money(price_eur),
        status="aktivni",
        description=description.strip() or None,
        created_at=now_utc(), updated_at=now_utc(),
    )
    db.add(listing)
    db.commit()
    flash(request, "Oglas objavljen.", "success")
    return RedirectResponse(f"/listings/{listing.id}", status_code=303)

@router.get("/listings/{listing_id}/edit")
def seller_listing_edit_form(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    listing = db.get(Listing, listing_id)
    if listing is None or listing.seller_id != user.id:
        raise HTTPException(404, "Oglas ne obstaja.")
    if listing.status == "prodan":
        flash(request, "Prodana oglasa ni mogoče urejati.", "error")
        return RedirectResponse("/seller/listings", status_code=303)
    return templates.TemplateResponse(
        request,
        "seller_listing_form.html",
        _listing_form_ctx(request, db, listing, f"/seller/listings/{listing.id}/edit"),
    )

@router.post("/listings/{listing_id}/edit")
async def seller_listing_edit(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
    make: str = Form(""),
    model: str = Form(""),
    year: str = Form(""),
    mileage_km: str = Form(""),
    fuel: str = Form(""),
    transmission: str = Form(""),
    price_eur: str = Form(""),
    description: str = Form(""),
):
    listing = db.get(Listing, listing_id)
    if listing is None or listing.seller_id != user.id:
        raise HTTPException(404, "Oglas ne obstaja.")
    if listing.status == "prodan":
        flash(request, "Prodana oglasa ni mogoče urejati.", "error")
        return RedirectResponse("/seller/listings", status_code=303)

    fields = {
        "make": make.strip(), "model": model.strip(), "year": year,
        "mileage_km": mileage_km, "fuel": fuel, "transmission": transmission,
        "price_eur": price_eur,
    }
    error = valid_listing_form(fields)
    if error:
        flash(request, error, "error")
        return RedirectResponse(f"/seller/listings/{listing.id}/edit", status_code=303)

    listing.make, listing.model = fields["make"], fields["model"]
    listing.year, listing.mileage_km = int(year), int(mileage_km)
    listing.fuel, listing.transmission = fuel, transmission
    listing.price_eur = parse_money(price_eur)
    listing.description = description.strip() or None
    listing.updated_at = now_utc()
    db.commit()
    flash(request, "Oglas posodobljen.", "success")
    return RedirectResponse(f"/listings/{listing.id}", status_code=303)

@router.post("/listings/{listing_id}/delete")
async def seller_listing_delete(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    listing = db.get(Listing, listing_id)
    if listing is None or listing.seller_id != user.id:
        raise HTTPException(404, "Oglas ne obstaja.")
    db.delete(listing)
    db.commit()
    flash(request, "Oglas izbrisan.", "success")
    return RedirectResponse("/seller/listings", status_code=303)

