# 0002 – Organizacija kode po vlogah z uporabo routerjev

## Status

Sprejeto

## Kontekst in problem

Aplikacija ima tri različne vloge (kupec, prodajalec, admin) z različnimi pogledi, pravicami in tokovi. Koda mora biti organizirana tako, da je pregledna in da razvijalec hitro najde ustrezen del. Vprašanje: kako razdeliti FastAPI kodo – po plasteh (routes, models, templates) ali po funkcionalnih sklopih (vlogah)?

## Odločitveni dejavniki

- Jasnost mej med vlogami
- Preglednost pri iskanju kode
- Enostavnost dodajanja novih vlog
- Preprečevanje nenamernega dostopa do tujih funkcionalnosti

## Obravnavane alternative

1. Routerji po vlogah: `auth`, `public`, `buyer`, `seller`, `admin`
2. En sam router z eno `routes.py` datoteko
3. Routerji po funkcionalnostih (npr. `listings`, `offers`, `users`)
4. Routerji po arhitekturnih plasteh (npr. `views`, `api`)

## Odločitev

Izbrana možnost: **routerji po vlogah**.

Vsaka vloga ima svoj FastAPI `APIRouter` z lastnimi pogledi in predlogami. Skupne funkcije (prijava, registracija) so v ločenem `auth` routerju, javno dostopni pogledi (seznam oglasov, detajl oglasa, profil prodajalca) pa v `public` routerju. To odraža dejansko strukturo pravic v aplikaciji in omogoča, da pri razvoju vedno delaš znotraj ene mape.

## Posledice

- **Dobro:** Meje med vlogami so jasne že iz strukture map.
- **Dobro:** Iskanje kode je intuitivno – za kupčevo stran odpreš mapo `routers/buyer.py`.
- **Dobro:** Preverjanje pravic je mogoče centralizirati v FastAPI dependency funkciji (`require_role("seller")`), ki jo router uporabi na ravni `APIRouter(dependencies=[...])`.
- **Slabo:** Skupna logika (npr. obrazci, ki jih uporablja več vlog) mora biti skrbno umeščena; sicer lahko pride do podvajanja.
- **Slabo:** Če se kasneje doda nova vloga, je treba ustvariti nov router in poskrbeti za registracijo v aplikaciji.

## Prednosti in slabosti možnosti

### Routerji po vlogah

- Dobro, ker je poravnava s poslovnimi mejami naravna.
- Dobro, ker je preverjanje pravic enostavno – router je "svoj" za vlogo.
- Slabo, ker skupne komponente (npr. skupni obrazci za več vlog) zahtevajo dodatno mesto.

### En sam router

- Dobro, ker je najmanj datotek.
- Slabo, ker `routes.py` hitro naraste v stotine vrstic in postane nepregleden.

### Routerji po funkcionalnostih

- Dobro, ker je primerno za projekte z veliko funkcionalnostmi na vlogo.
- Slabo, ker je za ta projekt manj naravna delitev – funkcionalnosti so tesno vezane na vlogo.

### Routerji po plasteh

- Dobro, ker gre za klasično MVC delitev.
- Slabo, ker se vsaka sprememba ene funkcionalnosti dotakne več map in povečuje kognitivno obremenitev.

## Več informacij

- [FastAPI – Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- Povezano z ADR [0001](0001-use-server-rendered-monolith.md).
