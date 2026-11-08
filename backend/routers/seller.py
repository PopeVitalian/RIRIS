"""Prodajalčeve poti: upravljanje oglasov in ponudb."""
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..auth import ctx, flash, require_role
from ..models import Listing, Offer, User
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

@router.get("/dashboard")
def seller_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    now = now_utc()
    thirty = now - timedelta(days=30)

    active_count = db.scalar(
        select(func.count()).select_from(Listing).where(
            Listing.seller_id == user.id, Listing.status == "aktivni"
        )
    ) or 0
    recent_offers = db.scalar(
        select(func.count()).select_from(Offer).join(Listing, Offer.listing_id == Listing.id)
        .where(Listing.seller_id == user.id, Offer.created_at >= thirty)
    ) or 0
    accepted_offers = db.scalar(
        select(func.count()).select_from(Offer).join(Listing, Offer.listing_id == Listing.id)
        .where(
            Listing.seller_id == user.id,
            Offer.status == "accepted",
            Offer.decided_at >= thirty,
        )
    ) or 0

    my_listings = db.scalars(
        select(Listing).where(Listing.seller_id == user.id)
        .order_by(Listing.created_at.desc()).limit(10)
    ).all()

    return templates.TemplateResponse(
        request,
        "seller_dashboard.html",
        {
            **ctx(request, db),
            "active_count": active_count,
            "recent_offers": recent_offers,
            "accepted_offers": accepted_offers,
            "my_listings": my_listings,
        },
    )

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

@router.post("/listings/{listing_id}/sold")
async def seller_listing_sold(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    listing = db.get(Listing, listing_id)
    if listing is None or listing.seller_id != user.id:
        raise HTTPException(404, "Oglas ne obstaja.")
    if listing.status != "rezerviran":
        flash(request, "Samo rezerviran oglas lahko označite kot prodan.", "error")
        return RedirectResponse("/seller/listings", status_code=303)
    listing.status = "prodan"
    listing.updated_at = now_utc()
    db.commit()
    flash(request, "Oglas označen kot prodan.", "success")
    return RedirectResponse("/seller/listings", status_code=303)

@router.get("/offers")
def seller_offers(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    offers = db.scalars(
        select(Offer).join(Listing, Offer.listing_id == Listing.id)
        .where(Listing.seller_id == user.id)
        .order_by(Offer.created_at.desc())
    ).all()

    grouped: dict[int, dict] = {}
    for o in offers:
        entry = grouped.setdefault(o.listing_id, {"listing": o.listing, "offers": []})
        entry["offers"].append(o)
    groups = sorted(
        grouped.values(), key=lambda g: g["listing"].created_at, reverse=True
    )
    return templates.TemplateResponse(
        request, "seller_offers.html", {**ctx(request, db), "groups": groups}
    )

@router.post("/offers/{offer_id}/accept")
async def seller_offer_accept(
    request: Request,
    offer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    offer = db.get(Offer, offer_id)
    if offer is None or offer.listing.seller_id != user.id:
        raise HTTPException(404, "Ponudba ne obstaja.")
    if offer.status != "pending":
        flash(request, "Ta ponudba ni več v čakanju.", "error")
        return RedirectResponse("/seller/offers", status_code=303)
    if offer.listing.status != "aktivni":
        flash(request, "Oglas ni več aktiven.", "error")
        return RedirectResponse("/seller/offers", status_code=303)

    now = now_utc()
    try:
        # (a) izbrana ponudba -> accepted
        offer.status = "accepted"
        offer.decided_at = now
        # (b) vse ostale pending ponudbe istega oglasa -> rejected
        db.execute(
            update(Offer)
            .where(
                Offer.listing_id == offer.listing_id,
                Offer.id != offer.id,
                Offer.status == "pending",
            )
            .values(status="rejected", decided_at=now)
        )
        # (c) oglas -> rezerviran
        offer.listing.status = "rezerviran"
        offer.listing.updated_at = now
        db.commit()
        flash(request, "Ponudba sprejeta. Ostale ponudbe so samodejno zavrnjene.", "success")
    except IntegrityError:
        # edinstven delni indeks prepreči dve accepted ponudbi na istem oglasu
        db.rollback()
        flash(request, "Oglas je bil v vmesnem času že rezerviran.", "error")
    return RedirectResponse("/seller/offers", status_code=303)

@router.post("/offers/{offer_id}/reject")
async def seller_offer_reject(
    request: Request,
    offer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    offer = db.get(Offer, offer_id)
    if offer is None or offer.listing.seller_id != user.id:
        raise HTTPException(404, "Ponudba ne obstaja.")
    if offer.status != "pending":
        flash(request, "Ta ponudba ni več v čakanju.", "error")
        return RedirectResponse("/seller/offers", status_code=303)
    offer.status = "rejected"
    offer.decided_at = now_utc()
    db.commit()
    flash(request, "Ponudba zavrnjena.", "success")
    return RedirectResponse("/seller/offers", status_code=303)
