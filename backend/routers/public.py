"""Javni pogledi: seznam oglasov, detajl, profil prodajalca, JSON API."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..auth import ctx, get_current_user
from ..models import Listing, User
from ..settings import FUELS, PER_PAGE, get_db, parse_money, templates

router = APIRouter()

@router.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/listings", status_code=303)

@router.get("/listings")
def list_listings(
    request: Request,
    db: Session = Depends(get_db),
    q: str = Query("", max_length=60),
    fuel: str = Query("", max_length=20),
    min_price: str = Query(""),
    max_price: str = Query(""),
    page: int = Query(1, ge=1),
):
    stmt = select(Listing).where(Listing.status == "aktivni")
    if q:
        stmt = stmt.where(or_(Listing.make.ilike(f"%{q}%"), Listing.model.ilike(f"%{q}%")))
    if fuel and fuel in FUELS:
        stmt = stmt.where(Listing.fuel == fuel)
    min_p = parse_money(min_price) if min_price else None
    if min_p is not None:
        stmt = stmt.where(Listing.price_eur >= min_p)
    max_p = parse_money(max_price) if max_price else None
    if max_p is not None:
        stmt = stmt.where(Listing.price_eur <= max_p)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    last_page = max(1, -(-total // PER_PAGE))
    page = min(page, last_page)

    listings = db.scalars(
        stmt.order_by(Listing.created_at.desc(), Listing.id.desc())
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
    ).all()

    prev_url = (
        str(request.url.include_query_params(page=page - 1)) if page > 1 else None
    )
    next_url = (
        str(request.url.include_query_params(page=page + 1))
        if page < last_page else None
    )

    return templates.TemplateResponse(
        request,
        "listings.html",
        {
            **ctx(request, db),
            "listings": listings,
            "q": q,
            "fuel": fuel,
            "min_price": min_price,
            "max_price": max_price,
            "page": page,
            "last_page": last_page,
            "total": total,
            "prev_url": prev_url,
            "next_url": next_url,
            "fuels": FUELS,
        },
    )

@router.get("/listings/{listing_id}")
def show_listing(request: Request, listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if listing is None or listing.status == "blokiran":
        raise HTTPException(404, "Oglas ne obstaja.")

    user = get_current_user(request, db)
    my_offer = None

    return templates.TemplateResponse(
        request,
        "listing_detail.html",
        {**ctx(request, db), "listing": listing, "my_offer": my_offer},
    )

@router.get("/sellers/{seller_id}")
def show_seller(request: Request, seller_id: int, db: Session = Depends(get_db)):
    seller = db.get(User, seller_id)
    if seller is None or seller.role != "seller" or seller.is_blocked:
        raise HTTPException(404, "Prodajalec ne obstaja.")
    listings = db.scalars(
        select(Listing)
        .where(Listing.seller_id == seller.id, Listing.status == "aktivni")
        .order_by(Listing.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        request,
        "seller_public.html",
        {**ctx(request, db), "seller": seller, "listings": listings},
    )
