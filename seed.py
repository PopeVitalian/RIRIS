"""Napolni bazo z realističnimi podatki za AvtoTrg.

Zagon:  python seed.py
Ustvari:
  * 5 demo računov s fiksnimi gesli (admin, 2 prodajalca, 2 kupca),
  * 30 naključnih prodajalcev in 50 naključnih kupcev (geslo "demo1234"),
  * ~800 oglasov z realistično povezanimi atributi,
  * ~1500 ponudb z različnimi statusi.

Podatki so deterministični (fiksno seme).
"""

import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from faker import Faker
from sqlalchemy import func, insert, select

from backend.models import Listing, Offer, User, hash_password
from backend.settings import FUELS, TRANSMISSIONS, engine

Faker.seed(42)
random.seed(42)

fake = Faker("sl_SI")

CITIES = [
    "Ljubljana", "Maribor", "Celje", "Kranj", "Velenje", "Koper", "Nova Gorica",
    "Novo mesto", "Ptuj", "Kamnik", "Trbovlje", "Jesenice", "Murska Sobota",
    "Domžale", "Škofja Loka", "Hrastnik", "Logatec", "Kočevje", "Sežana", "Postojna",
]

MODELS = {
    "Renault": ["Clio", "Mégane", "Captur", "Twingo"],
    "Peugeot": ["208", "308", "3008", "Partner"],
    "Citroën": ["C3", "C4", "Berlingo"],
    "Volkswagen": ["Golf", "Polo", "Passat", "T-Roc", "Touran"],
    "Škoda": ["Octavia", "Fabia", "Superb", "Kamiq", "Kodiaq"],
    "Opel": ["Astra", "Corsa", "Insignia", "Mokka"],
    "Dacia": ["Sandero", "Duster", "Dokker"],
    "Toyota": ["Yaris", "Corolla", "RAV4", "Avensis"],
    "Hyundai": ["i30", "i20", "Tucson", "i10"],
    "Kia": ["Rio", "Ceed", "Sportage", "Picanto"],
    "Fiat": ["Panda", "500", "Tipo", "Punto"],
    "BMW": ["318d", "320d", "X3", "520d"],
    "Audi": ["A3", "A4", "Q5", "A6"],
    "Mercedes-Benz": ["A 180", "C 220", "E 220"],
    "Ford": ["Fiesta", "Focus", "Mondeo", "Kuga"],
}
MAKE_WEIGHTS = [9, 8, 5, 14, 13, 8, 7, 6, 5, 5, 5, 5, 4, 3, 3]

PRICE_TIER = {"budget": (9_000, 16_000), "mid": (16_000, 32_000), "premium": (32_000, 70_000)}
TIERS = ["budget", "mid", "mid", "mid", "premium"]

FUEL_WEIGHTS = [48, 34, 8, 5, 5]

DESCRIPTIONS = [
    "Servisirano pri pooblaščenem serviserju, vsa dokumentacija.",
    "Prvi lastnik, garažno parkirano.",
    "Brez poškodb, original lak.",
    "Zimske in letne pnevmatike vred.",
    "Redno menjano olje, zadnji servis pred 2.000 km.",
    "Neprekušen, slovenski avto.",
    "Možnost menjave za novejši model.",
    "Zelo varčna vožnja, motor brez napak.",
    "Voznik nekadilec, notranjost brez madežev.",
    "Hitra prodaja zaradi selitve v tujino.",
]

OFFER_MESSAGES = [
    "Ponujam takoj, plačam v gotovini.",
    "Ali je možno ogledati v soboto?",
    "Kaj je vaša zadnja cena?",
    "Sem resen kupec, lahko pridem jutri.",
    "Ponujam dogovorjen znesek, prevzem v enem tednu.",
    "Bi zamenjali za moj avto + doplačilo?",
    "Zanima me servisna zgodovina, prosim.",
]

def unique_emails(n: int, prefix: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    i = 0
    while len(out) < n:
        email = f"{prefix}{i}@avtotrg.si"
        i += 1
        if email not in seen:
            seen.add(email)
            out.append(email)
    return out

def slovenian_phone() -> str:
    return f"0{random.randint(31, 70)} {random.randint(100, 999)} {random.randint(100, 999)}"

def make_demo_users() -> tuple[list[dict], list[dict]]:
    """Vrne (admins+sellers, buyers)."""
    now = datetime.now(timezone.utc)

    staff_rows = [
        {
            "email": "admin@avtotrg.si",
            "password_hash": hash_password("admin123"),
            "full_name": "Admin AvtoTrg",
            "phone": "01 234 56 78",
            "city": "Ljubljana",
            "role": "admin",
            "is_dealer": False,
            "is_blocked": False,
            "created_at": now - timedelta(days=180),
        },
        {
            "email": "avtohisa@avtotrg.si",
            "password_hash": hash_password("seller123"),
            "full_name": "Avtohiša Novak",
            "phone": "01 111 22 33",
            "city": "Ljubljana",
            "role": "seller",
            "is_dealer": True,
            "is_blocked": False,
            "created_at": now - timedelta(days=150),
        },
        {
            "email": "janez@avtotrg.si",
            "password_hash": hash_password("seller123"),
            "full_name": "Janez Novak",
            "phone": "041 111 222",
            "city": "Maribor",
            "role": "seller",
            "is_dealer": False,
            "is_blocked": False,
            "created_at": now - timedelta(days=120),
        },
    ]

    buyer_rows = [
        {
            "email": "kupec@avtotrg.si",
            "password_hash": hash_password("buyer123"),
            "full_name": "Miha Kupec",
            "phone": "051 333 444",
            "city": "Ljubljana",
            "role": "buyer",
            "is_dealer": False,
            "is_blocked": False,
            "created_at": now - timedelta(days=90),
        },
        {
            "email": "maja@avtotrg.si",
            "password_hash": hash_password("buyer123"),
            "full_name": "Maja Kovač",
            "phone": "070 555 666",
            "city": "Celje",
            "role": "buyer",
            "is_dealer": False,
            "is_blocked": False,
            "created_at": now - timedelta(days=60),
        },
    ]

    return staff_rows, buyer_rows

def make_random_users(n_sellers: int, n_buyers: int) -> tuple[list[dict], list[dict]]:
    demo_hash = hash_password("demo1234")
    now = datetime.now(timezone.utc)

    seller_emails = unique_emails(n_sellers, "prodajalec")
    buyer_emails = unique_emails(n_buyers, "kupec")

    sellers = []
    for email in seller_emails:
        is_dealer = random.random() < 0.3
        if is_dealer:
            name = random.choice(
                [
                    f"Avtohiša {fake.last_name()}",
                    f"Avtocenter {fake.last_name()}",
                    f"{fake.last_name()} avto d.o.o.",
                ]
            )
        else:
            name = fake.name()
        sellers.append(
            {
                "email": email,
                "password_hash": demo_hash,
                "full_name": name,
                "phone": slovenian_phone(),
                "city": random.choice(CITIES),
                "role": "seller",
                "is_dealer": is_dealer,
                "is_blocked": False,
                "created_at": now - timedelta(days=random.randint(10, 400)),
            }
        )

    buyers = []
    for email in buyer_emails:
        buyers.append(
            {
                "email": email,
                "password_hash": demo_hash,
                "full_name": fake.name(),
                "phone": slovenian_phone(),
                "city": random.choice(CITIES),
                "role": "buyer",
                "is_dealer": False,
                "is_blocked": False,
                "created_at": now - timedelta(days=random.randint(5, 300)),
            }
        )

    return sellers, buyers

def make_listing_rows(seller_ids: list[int], n: int) -> list[dict]:
    counts = {}
    for sid in seller_ids:
        big = (sid % 5 == 0)
        counts[sid] = random.randint(15, 40) if big else random.randint(1, 3)

    total = sum(counts.values())
    ids = list(counts)
    while total > n:
        sid = random.choice(ids)
        if counts[sid] > 1:
            counts[sid] -= 1
            total -= 1
    while total < n:
        sid = random.choice(ids)
        counts[sid] += 1
        total += 1

    rows = []
    now = datetime.now(timezone.utc)
    for sid, count in counts.items():
        for _ in range(count):
            make = random.choices(list(MODELS), weights=MAKE_WEIGHTS, k=1)[0]
            model = random.choice(MODELS[make])
            year = random.randint(2005, 2024)
            age = 2025 - year
            mileage = max(500, int(age * 14_000 * random.uniform(0.6, 1.4)))
            tier = random.choice(TIERS)
            low, high = PRICE_TIER[tier]
            new_price = random.uniform(low, high)
            price = new_price * (0.86 ** age) * (1 - min(0.25, mileage / 1_600_000))
            price = max(500, int(round(price / 50) * 50))
            created = now - timedelta(
                days=random.randint(0, 365), minutes=random.randint(0, 60 * 24)
            )
            status = random.choices(
                ["aktivni", "rezerviran", "prodan"],
                weights=[80, 8, 12],
                k=1,
            )[0]
            desc = " ".join(random.sample(DESCRIPTIONS, k=random.randint(1, 3)))
            km_str = f"{mileage:,}".replace(",", ".")
            rows.append(
                {
                    "seller_id": sid,
                    "make": make, "model": model, "year": year,
                    "mileage_km": mileage,
                    "fuel": random.choices(FUELS, weights=FUEL_WEIGHTS, k=1)[0],
                    "transmission": random.choices(TRANSMISSIONS, weights=[45, 55], k=1)[0],
                    "price_eur": Decimal(price).quantize(Decimal("0.01")),
                    "status": status,
                    "description": f"{make} {model}, letnik {year}, {km_str} km. {desc}",
                    "created_at": created, "updated_at": created,
                }
            )
    return rows

def make_offer_rows(listing_ids: list[int], buyer_ids: list[int], n: int) -> list[dict]:
    """Vsaka ponudba gre na naključen oglas; statusi uravnoteženi."""
    now = datetime.now(timezone.utc)
    rows = []
    for _ in range(n):
        listing_id = random.choice(listing_ids)
        buyer_id = random.choice(buyer_ids)
        status = random.choices(
            ["pending", "accepted", "rejected", "withdrawn"],
            weights=[50, 5, 30, 15],
            k=1,
        )[0]
        created = now - timedelta(
            days=random.randint(0, 90), minutes=random.randint(0, 60 * 24)
        )
        decided = None
        if status != "pending":
            decided = created + timedelta(hours=random.randint(1, 72))
            if decided > now:
                decided = now - timedelta(minutes=random.randint(1, 60))
        rows.append(
            {
                "listing_id": listing_id,
                "buyer_id": buyer_id,
                "amount_eur": Decimal(random.randint(500, 60000)).quantize(Decimal("0.01")),
                "message": random.choice(OFFER_MESSAGES),
                "status": status,
                "created_at": created,
                "decided_at": decided,
            }
        )
    return rows

def main() -> None:
    from sqlalchemy import inspect

    inspector = inspect(engine)
    missing = [
        t for t in ("users", "listings", "offers") if not inspector.has_table(t)
    ]
    if missing:
        raise SystemExit(
            f"Tabel {missing} ni v bazi. Najprej zaženi schema.sql (glej README)."
        )

    # Če baza že ima uporabnike, ne seedamo znova.
    with engine.connect() as conn:
        existing = conn.scalar(select(func.count()).select_from(User))
    if existing and existing > 0:
        print(f"V bazi je že {existing} uporabnikov. Seed preskočen.")
        return

    staff_rows, buyer_rows = make_demo_users()
    random_sellers, random_buyers = make_random_users(n_sellers=30, n_buyers=50)

    seller_rows = staff_rows[1:] + random_sellers  # [0] je admin
    admin_rows = [staff_rows[0]]
    all_buyers = buyer_rows + random_buyers

    print(f"Vstavljam {len(admin_rows) + len(seller_rows) + len(all_buyers)} uporabnikov ...")
    with engine.begin() as conn:
        conn.execute(insert(User), admin_rows + seller_rows + all_buyers)
        seller_ids = [
            r[0] for r in conn.execute(
                select(User.id).where(User.role == "seller").order_by(User.id)
            ).all()
        ]
        buyer_ids = [
            r[0] for r in conn.execute(
                select(User.id).where(User.role == "buyer").order_by(User.id)
            ).all()
        ]

    listing_rows = make_listing_rows(seller_ids, n=800)
    print(f"Vstavljam {len(listing_rows)} oglasov ...")
    CHUNK = 1000
    with engine.begin() as conn:
        for i in range(0, len(listing_rows), CHUNK):
            conn.execute(insert(Listing), listing_rows[i : i + CHUNK])
        listing_ids = [
            r[0] for r in conn.execute(select(Listing.id).order_by(Listing.id)).all()
        ]

    offer_rows = make_offer_rows(listing_ids, buyer_ids, n=1500)
    # En accepted na oglas; naključne accepted na istem oglasu -> rejected.
    seen_accepted: set[int] = set()
    for row in offer_rows:
        if row["status"] == "accepted":
            if row["listing_id"] in seen_accepted:
                row["status"] = "rejected"
            else:
                seen_accepted.add(row["listing_id"])

    print(f"Vstavljam {len(offer_rows)} ponudb ...")
    with engine.begin() as conn:
        for i in range(0, len(offer_rows), CHUNK):
            conn.execute(insert(Offer), offer_rows[i : i + CHUNK])

    with engine.connect() as conn:
        n_u = conn.scalar(select(func.count()).select_from(User))
        n_l = conn.scalar(select(func.count()).select_from(Listing))
        n_o = conn.scalar(select(func.count()).select_from(Offer))
    print(f"Končano. V bazi je {n_u} uporabnikov, {n_l} oglasov, {n_o} ponudb.")

if __name__ == "__main__":
    main()
