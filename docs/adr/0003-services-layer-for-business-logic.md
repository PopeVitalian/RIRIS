# 0003 – Ločen services sloj za poslovno logiko

## Status

Sprejeto

## Kontekst in problem

Nekatera poslovna pravila so netrivialna in jih uporablja več pogledov hkrati: sprejem ponudbe z atomsko zavrnitvijo ostalih, prehod oglasa med statusi ob sprejemu/prodaji, preverjanje blokade uporabnika ob prijavi in ob oddaji ponudbe. Če takšno logiko zapišemo neposredno v route funkcije, se podvaja in jo je težko testirati.

## Odločitveni dejavniki

- Možnost ponovne uporabe logike na več mestih
- Testabilnost poslovne logike brez HTTP konteksta
- Preglednost route funkcij
- Enostavnost vzdrževanja ob spremembah pravil

## Obravnavane alternative

1. Poslovna logika v route funkcijah (vse v `routes.py`)
2. Poslovna logika v modelih (metode na SQLAlchemy modelih)
3. Ločen `services/` sloj med route in modeli
4. Zunanja knjižnica za pravila (npr. `business-rules`)

## Odločitev

Izbrana možnost: **ločen `services/` sloj**.

Vsaka zaokrožena poslovna operacija (npr. `accept_offer`, `reject_offer`, `withdraw_offer`, `transition_listing_status`, `check_block_status`) je funkcija v `services/`, ki prejme potrebne modele in parametre ter vrne rezultat. Route funkcije ostanejo tanke – preverijo pravice, pokličejo service, pripravijo predlogo.

Posebej pomembno: **sprejem ponudbe** ni preprost `UPDATE`. Zahteva atomsko transakcijo, ki (a) nastavi izbrano ponudbo v `accepted`, (b) vse ostale `pending` ponudbe istega oglasa v `rejected`, (c) oglas v `rezerviran`. Ta logika je v `services/offers.py::accept_offer()` in je testabilna brez HTTP.

## Posledice

- **Dobro:** Logika je testabilna brez zagona FastAPI aplikacije.
- **Dobro:** Pravila so zapisana na enem mestu in jih je enostavno spremeniti.
- **Dobro:** Route funkcije ostanejo kratke in pregledne.
- **Slabo:** Več datotek in posredni sloj med HTTP in ORM.
- **Slabo:** Za zelo preprosta pravila (npr. preverjanje, ali je uporabnik prijavljen) uvajanja service funkcije ni smiselno; potrebna je presoja.

## Prednosti in slabosti možnosti

### Logika v route funkcijah

- Dobro, ker je manj datotek.
- Slabo, ker prihaja do podvajanja in težavnega testiranja.

### Logika v modelih

- Dobro, ker je blizu podatkom.
- Slabo, ker modeli postanejo debeli in mešajo perzistenco s poslovnimi pravili, kar otežuje testiranje in vzdrževanje.

### Ločen services sloj

- Dobro, ker je meja med HTTP in poslovno logiko jasna.
- Dobro, ker je testiranje enostavno.
- Slabo, ker dodaja raven abstrakcije za majhen projekt.

### Zunanja knjižnica

- Dobro, ker so morda pravila standardizirana.
- Slabo, ker prinaša dodatno odvisnost in učno krivuljo za enostaven obseg pravil.

## Več informacij

- [FastAPI – Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLAlchemy – Session and Transaction](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)
- Povezano z ADR [0001](0001-use-server-rendered-monolith.md) in [0002](0002-organize-code-by-role-routers.md).
