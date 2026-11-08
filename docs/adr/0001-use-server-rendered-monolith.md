# 0001 – Uporaba strežniško izrisanega monolita

## Status

Sprejeto

## Kontekst in problem

AvtoTrg je spletna aplikacija za trgovanje z rabljenimi avtomobili z jasno omejenim obsegom (MVP s 7 funkcionalnostmi) in ekipo enega razvijalca. Potrebujemo arhitekturo, ki omogoča hiter razvoj, enostavno nameščanje in preprosto vzdrževanje, hkrati pa mora podpirati tri različne uporabniške vloge (kupec, prodajalec, admin) in poglede, ki se razlikujejo glede na vlogo.

Ključno vprašanje: ali naj aplikacijo zgradimo kot monolit s strežniškim izrisom ali kot ločen frontend (SPA) in backend (REST API)?

## Odločitveni dejavniki

- Velikost projekta (MVP, en razvijalec)
- Hitrost razvoja in enostavnost nameščanja
- Število uporabniških vlog in dinamičnost pogledov
- Zahteve po avtentikaciji in sejah
- Vzdrževalna obremenitev

## Obravnavane alternative

1. FastAPI + Jinja2 strežniško izrisan monolit
2. Ločen SPA frontend (React/Vue) + FastAPI REST API
3. Next.js full-stack (Node)
4. Django monolit

## Odločitev

Izbrana možnost: **FastAPI + Jinja2 strežniško izrisan monolit**.

Zaradi majhnega obsega projekta in enega razvijalca ločevanje frontenda in backenda ne prinaša bistvene vrednosti, hkrati pa zahteva dva ločena projekta, dve razvojni okolji in vzdrževanje API pogodbe. Strežniški izris z Jinja2 predlogami zadošča vsem funkcionalnostim, saj so pogledi pretežno obrazci in seznami, ki se razlikujejo le po vlogi prijavljenega uporabnika. Starlette `SessionMiddleware` s piškotki pokrije avtentikacijo brez dodatne kompleksnosti.

## Posledice

- **Dobro:** Manj gibljivih delov – ena aplikacija, ena baza, ena namestitev.
- **Dobro:** Izris pogledov glede na vlogo je neposreden (Jinja2 predloge se odločajo po `current_user.role`).
- **Dobro:** Ena koda, en sklop odvisnosti in ena baza pomenijo, da je vzdrževanje obvladljivo tudi za ekipo enega razvijalca.
- **Slabo:** Tesna povezanost med prikazom in poslovno logiko otežuje kasnejšo zamenjavo frontenda (npr. za native mobilno aplikacijo).
- **Slabo:** Če se kasneje doda SPA, bo treba dodati REST API plast in prenoviti poglede.
- **Slabo:** Manj primerno za interaktivne elemente v živo – to bo rešeno s periodičnim osveževanjem strani.

## Prednosti in slabosti možnosti

### FastAPI + Jinja2 strežniško izrisan monolit

- Dobro, ker je hitra izdelava, malo konfiguracije in enostavno nameščanje.
- Dobro, ker je avtentikacija s sejami trivialna.
- Slabo, ker je uporabniški vmesnik manj interaktiven brez JavaScripta.

### SPA + REST API

- Dobro, ker loči skrbi in omogoča bogatejši UI.
- Slabo, ker sta dva projekta, več konfiguracije, potreba po API pogodbi in ločenem avtentikacijskem toku (JWT ali piškotki).
- Slabo, ker je bistveno več dela za isti MVP obseg.

### Next.js full-stack

- Dobro, ker je moderno in integrira frontend in backend.
- Slabo, ker zahteva Node in JavaScript ekosistem, kar je za ekipo, ki je doma v Pythonu, dodatna ovira.

### Django monolit

- Dobro, ker prinaša admin, ORM in migracije "iz škatlice".
- Slabo, ker je težji okvir z več vgrajenimi konvencijami; za majhen projekt prevelika teža in manj prilagodljivosti.

## Več informacij

- [FastAPI dokumentacija](https://fastapi.tiangolo.com/)
- [Jinja2 dokumentacija](https://jinja.palletsprojects.com/)
- Povezano z ADR [0002](0002-organize-code-by-role-routers.md) in [0003](0003-services-layer-for-business-logic.md).
