"""Kupčeve poti: oddaja ponudbe, pregled in umik."""
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..auth import ctx, flash, require_role
from ..models import Listing, Offer, User
from ..settings import OFFER_STATUSES, get_db, now_utc, parse_money, templates

router = APIRouter()

@router.post("/listings/{listing_id}/offers")
async def submit_offer(
    request: Request,
    listing_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("buyer")),
    amount_eur: str = Form(""),
    message: str = Form(""),
):
    listing = db.get(Listing, listing_id)
    if listing is None or listing.status != "aktivni":
        flash(request, "Oglas ni več aktiven.", "error")
        return RedirectResponse(f"/listings/{listing_id}", status_code=303)
    if listing.seller_id == user.id:
        flash(request, "Ne morete oddati ponudbe na lasten oglas.", "error")
        return RedirectResponse(f"/listings/{listing_id}", status_code=303)
    amount = parse_money(amount_eur)
    if amount is None or amount <= 0:
        flash(request, "Znesek mora biti pozitivno število.", "error")
        return RedirectResponse(f"/listings/{listing_id}", status_code=303)

    existing = db.scalar(
        select(Offer).where(
            Offer.listing_id == listing.id,
            Offer.buyer_id == user.id,
            Offer.status == "pending",
        )
    )
    if existing:
        flash(request, "Že imate ponudbo v čakanju na tem oglasu.", "error")
        return RedirectResponse(f"/listings/{listing_id}", status_code=303)

    offer = Offer(
        listing_id=listing.id,
        buyer_id=user.id,
        amount_eur=amount,
        message=message.strip() or None,
        status="pending",
        created_at=now_utc(),
    )
    db.add(offer)
    db.commit()
    flash(request, "Ponudba oddana. Spremljate jo lahko v svojih ponudbah.", "success")
    return RedirectResponse("/buyer/offers", status_code=303)

@router.get("/buyer/dashboard")
def buyer_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("buyer")),
):
    recent = db.scalars(
        select(Offer)
        .where(Offer.buyer_id == user.id)
        .order_by(Offer.created_at.desc())
        .limit(10)
    ).all()
    counts = {
        "pending": db.scalar(
            select(func.count()).select_from(Offer).where(
                Offer.buyer_id == user.id, Offer.status == "pending"
            )
        ) or 0,
        "accepted": db.scalar(
            select(func.count()).select_from(Offer).where(
                Offer.buyer_id == user.id, Offer.status == "accepted"
            )
        ) or 0,
    }
    return templates.TemplateResponse(
        request,
        "buyer_dashboard.html",
        {**ctx(request, db), "recent": recent, "counts": counts},
    )

@router.get("/buyer/offers")
def buyer_offers(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("buyer")),
    status: str = Query("", max_length=20),
):
    stmt = select(Offer).where(Offer.buyer_id == user.id)
    if status and status in OFFER_STATUSES:
        stmt = stmt.where(Offer.status == status)
    offers = db.scalars(stmt.order_by(Offer.created_at.desc())).all()
    return templates.TemplateResponse(
        request,
        "buyer_offers.html",
        {**ctx(request, db), "offers": offers, "status_filter": status, "statuses": OFFER_STATUSES},
    )

@router.post("/offers/{offer_id}/withdraw")
async def withdraw_offer(
    request: Request,
    offer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("buyer")),
):
    offer = db.get(Offer, offer_id)
    if offer is None or offer.buyer_id != user.id:
        raise HTTPException(404, "Ponudba ne obstaja.")
    if offer.status != "pending":
        flash(request, "Ponudbe ni več mogoče umakniti.", "error")
        return RedirectResponse("/buyer/offers", status_code=303)
    offer.status = "withdrawn"
    offer.decided_at = now_utc()
    db.commit()
    flash(request, "Ponudba umaknjena.", "success")
    return RedirectResponse("/buyer/offers", status_code=303)
