# 0004 – Izbira CockroachDB za shranjevanje podatkov

## Status

Sprejeto

## Kontekst in problem

Potrebujemo relacijsko podatkovno bazo, ki jo je mogoče zagnati lokalno med razvojem, podpira SQL in je dovolj zmogljiva za MVP, hkrati pa omogoča kasnejšo skalabilnost, če bi se projekt razširil. Odločitev vpliva na ORM plast (SQLAlchemy), migracije (Flask-Migrate) in način lokalnega zagona (Docker).

## Odločitveni dejavniki

- Podpora SQL in združljivost s SQLAlchemy
- Enostavno lokalno zaganjanje (najbolje v Dockerju)
- Izkušnje ekipe
- Možnost skaliranja v prihodnosti
- Vzdrževalna zahtevnost

## Obravnavane alternative

1. CockroachDB (lokalno v Dockerju)
2. PostgreSQL (lokalno v Dockerju)
3. SQLite (vgrajen v Python)
4. MySQL
5. MongoDB

## Odločitev

Izbrana možnost: **CockroachDB v Dockerju**.

CockroachDB je relacijska baza s SQL vmesnikom in dobrim ujemanjem s SQLAlchemy. Ker teče v Dockerju, je lokalni zagon enak ne glede na razvojno okolje. Izbrana je bila tudi zato, ker je bila uporabljena že v prejšnjem projektu in ker ponuja pot k skalabilnosti brez menjave baze, če bi se projekt razširil. Hkrati je cilj projekta tudi podrobneje spoznati CockroachDB.

## Posledice

- **Dobro:** SQL in SQLAlchemy delujeta brez prilagoditev.
- **Dobro:** Docker poskrbi za ponovljiv lokalni zagon.
- **Dobro:** Možnost skaliranja v prihodnosti brez menjave baze.
- **Slabo:** CockroachDB je težja in požrešnejša od SQLite, kar za MVP ni nujno potrebno.
- **Slabo:** Nekatere funkcije se razlikujejo od PostgreSQL; morebitne razlike bo treba upoštevati pri poizvedbah.
- **Slabo:** Za razvijalca, ki CockroachDB pozna manj dobro, je učna krivulja daljša kot pri PostgreSQL.

## Prednosti in slabosti možnosti

### CockroachDB

- Dobro, ker ponuja SQL, skalabilnost in Docker prijaznost.
- Dobro, ker imamo izkušnje iz prejšnjega projekta.
- Slabo, ker je poraba virov večja kot pri SQLite.

### PostgreSQL

- Dobro, ker je zrela, široko uporabljena in dobro poznana.
- Slabo, ker ne prinaša bistvene prednosti pred CockroachDB za ta obseg in ne omogoča tako enostavne poti do porazdeljene baze.

### SQLite

- Dobro, ker nič konfiguracije in je vgrajen v Python.
- Slabo, ker ni primeren za več hkratnih piscev in ne omogoča preproste poti do produkcijske baze.

### MySQL

- Dobro, ker je razširjen in dobro poznan.
- Slabo, ker v okolju Docker zahteva dodatno konfiguracijo in je v Python ekosistemu manj priljubljen kot PostgreSQL.

### MongoDB

- Dobro, ker ima prilagodljivo shemo.
- Slabo, ker ni relacijska baza, zato ne ustreza podatkovnemu modelu s tujimi ključi in transakcijami.

## Več informacij

- [CockroachDB dokumentacija](https://www.cockroachlabs.com/docs/)
- [SQLAlchemy dokumentacija](https://docs.sqlalchemy.org/)
- Povezano z ADR [0001](0001-use-server-rendered-monolith.md).
