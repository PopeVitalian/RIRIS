# AvtoTrg – spletna platforma za trgovanje z rabljenimi avtomobili (RIRIS)

Kupec odda **strukturirano ponudbo** na oglas, prodajalec jo **sprejme** (ob tem se vse ostale ponudbe na oglasu samodejno zavrnejo, oglas preide v `rezerviran`) ali **zavrne**. Po prodaji prodajalec oglas označi kot `prodan`.

## Tehnološki stack

| Plast | Tehnologija |
|---|---|
| Obličje | Jinja2 predloge (server-rendered) + CSS |
| Zaledje | Python 3.11+, FastAPI, SQLAlchemy 2.0 |
| Podatkovna baza | PostgreSQL 18 v Dockerju |
| Avtentikacija | Starlette `SessionMiddleware` + bcrypt |
| Testni podatki | Faker |

## Struktura

```

RIRIS/
├── backend/
│   ├── __init__.py
│   ├── app.py               FastAPI instance + middleware + exception handler
│   ├── settings.py          konfiguracija, baza, predloge, pomožne funkcije
│   ├── models.py            User, Listing, Offer + hash/verify_password
│   ├── auth.py              flash, get_current_user, require_role, ctx
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          register / login / logout
│       ├── public.py        seznam oglasov, detajl, profil prodajalca, JSON API
│       ├── buyer.py         oddaja ponudbe, pregled, umik
│       ├── seller.py        upravljanje oglasov in ponudb
│       └── admin.py         uporabniki, oglasi, blokade, vloge
├── frontend/
│   ├── static/style.css
│   └── templates/           vse Jinja2 predloge
├── docker-compose.yml
├── schema.sql               DDL: 5 enum tipov, 3 tabele, indeksi, CHECK omejitve
├── seed.py                  Faker demo podatki
├── run.py                   razvojni zagon
└── requirements.txt

```

## Zagon

```bash
# 1. Zaženi PostgreSQL
docker compose up -d

# 2. Namesti odvisnosti
conda activate RIRIS    # ali generično: python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Naloži shemo
docker exec -i avtotrg-postgres psql -U avtotrg -d avtotrg_db < schema.sql

# 4. Napolni demo podatke
python seed.py

# 5. Zaženi
python run.py            # http://127.0.0.1:8000
```

## Demo računi

| Vloga | E-pošta | Geslo |
|---|---|---|
| Admin | `admin@avtotrg.si` | `admin123` |
| Prodajalec (avtohiša) | `avtohisa@avtotrg.si` | `seller123` |
| Prodajalec (zasebnik) | `janez@avtotrg.si` | `seller123` |
| Kupec | `kupec@avtotrg.si` | `buyer123` |
| Kupec | `maja@avtotrg.si` | `buyer123` |

Naključni uporabniki imajo geslo `demo1234`.

## Vloge

| Vloga | Ključ | Lahko | Ne more |
|---|---|---|---|
| Kupec | `buyer` | Brska, filtrira, odda ponudbo, umakne svojo ponudbo | Ne objavlja oglasov, ne vidi tujih ponudb |
| Prodajalec | `seller` | Objavlja/ureja/briše svoje oglase, vidi prejete ponudbe, sprejema/zavrača | Ne vidi ponudb na tuje oglase |
| Admin | `admin` | Pregleduje uporabnike in oglase, blokira/odblokira, spreminja vloge | Ne kupuje, ne prodaja, ne blokira drugega admina |

## Poslovna pravila

### Sprejem ponudbe

Ob sprejemu ponudbe se v eni transakciji zgodi:

1. izbrana ponudba → `accepted`, `decided_at` = zdaj;
2. vse ostale `pending` ponudbe na istem oglasu → `rejected`, `decided_at` = zdaj;
3. oglas → `rezerviran`.

Varnost pred dvojnim sprejemom zagotavlja **edinstven delni indeks** `idx_offers_one_accepted_per_listing`. Če dva zahtevka hkrati poskušata sprejeti, drugi pade na `IntegrityError` in se rollback-a.

### Ostala pravila

- Kupec ne more oddati ponudbe na lasten oglas.
- Kupec ne more oddati ponudbe na oglas, ki ni `aktivni`.
- Kupec ne more imeti več kot ene `pending` ponudbe na istem oglasu.
- Ponudbo v statusu `pending` lahko kupec umakne (`withdrawn`).
- Oglas v `rezerviran` lahko prodajalec označi kot `prodan`.
- Prodana oglasa ni mogoče urejati.
- Blokiran uporabnik se ne more prijaviti.
- Admin ne more blokirati samega sebe, ne drugega admina, ne spremeniti lastne vloge.

