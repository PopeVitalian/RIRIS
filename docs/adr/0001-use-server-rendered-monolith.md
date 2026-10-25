# 0001 – Uporaba strežniško izrisanega monolita

## Status

Sprejeto

## Kontekst in problem

Parkelj je spletna aplikacija za upravljanje parkirišč z jasno omejenim obsegom (MVP z 11 funkcionalnostmi) in ekipo enega razvijalca. Potrebujemo arhitekturo, ki omogoča hiter razvoj, enostavno nameščanje in preprosto vzdrževanje, hkrati pa mora podpirati tri različne uporabniške vloge (voznik, operater, admin) in poglede, ki se razlikujejo glede na vlogo.

Ključno vprašanje: ali naj aplikacijo zgradimo kot monolit s strežniškim izrisom ali kot ločen frontend (SPA) in backend (REST API)?

## Odločitveni dejavniki

- Velikost projekta (MVP, en razvijalec)
- Hitrost razvoja in enostavnost nameščanja
- Število uporabniških vlog in dinamičnost pogledov
- Zahteve po avtentikaciji in sejah
- Vzdrževalna obremenitev

## Obravnavane alternative

1. Flask + Jinja strežniško izrisan monolit
2. Ločen SPA frontend (React/Vue) + Flask REST API
3. Next.js full-stack (Node)
4. Django monolit

## Odločitev

Izbrana možnost: **Flask + Jinja strežniško izrisan monolit**.

Zaradi majhnega obsega projekta in enega razvijalca ločevanje frontenda in backenda ne prinaša bistvene vrednosti, hkrati pa zahteva dva ločena projekta, dve razvojni okolji in vzdrževanje API pogodbe. Strežniški izris z Jinja predlogami zadošča vsem funkcionalnostim, saj so pogledi pretežno obrazci in seznami, ki se razlikujejo le po vlogi prijavljenega uporabnika. Flask-Login s sejami in piškotki pokrije avtentikacijo brez dodatne kompleksnosti.

## Posledice

- **Dobro:** Manj gibljivih delov – ena aplikacija, ena baza, ena namestitev.
- **Dobro:** Izris pogledov glede na vlogo je neposreden (Jinja predloge se odločajo po `current_user.role`).
- **Dobro:** Ena koda, en sklop odvisnosti in ena baza pomenijo, da je vzdrževanje obvladljivo tudi za ekipo enega razvijalca in da ni skrite kompleksnosti v API sloju, ki bi jo bilo treba sinhronizirati s frontendom.
- **Slabo:** Tesna povezanost med prikazom in poslovno logiko otežuje kasnejšo zamenjavo frontenda (npr. za native mobilno aplikacijo).
- **Slabo:** Če se kasneje doda SPA, bo treba dodati REST API plast in prenoviti poglede.
- **Slabo:** Manj primerno za interaktivne elemente v živo (npr. sprotno osveževanje zasedenosti brez ponovnega nalaganja strani) – to bo rešeno s periodičnim osveževanjem strani.

## Prednosti in slabosti možnosti

### Flask + Jinja strežniško izrisan monolit

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

- [Flask dokumentacija](https://flask.palletsprojects.com/)
- [Jinja dokumentacija](https://jinja.palletsprojects.com/)
- Povezano z ADR [0002](0002-organize-code-by-role-blueprints.md) in [0003](0003-services-layer-for-business-logic.md).
