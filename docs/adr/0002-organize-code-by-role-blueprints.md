# 0002 – Organizacija kode po vlogah z uporabo blueprintov

## Status

Sprejeto

## Kontekst in problem

Aplikacija ima štiri različne vloge (voznik, operater, lokalni admin in admin) z različnimi pogledi, pravicami in tokovi. Koda mora biti organizirana tako, da je pregledna in da razvijalec hitro najde ustrezen del. Vprašanje: kako razdeliti Flask kodo – po plasteh (routes, models, templates) ali po funkcionalnih sklopih (vlogah)?

## Odločitveni dejavniki

- Jasnost mej med vlogami
- Preglednost pri iskanju kode
- Enostavnost dodajanja novih vlog
- Preprečevanje nenamernega dostopa do tujih funkcionalnosti

## Obravnavane alternative

1. Blueprints po vlogah: `auth`, `driver`, `operator`, `admin`
2. En sam blueprint z eno `routes.py` datoteko
3. Blueprints po funkcionalnostih (npr. `sessions`, `vehicles`, `penalties`)
4. Blueprints po arhitekturnih plasteh (npr. `views`, `api`)

## Odločitev

Izbrana možnost: **blueprints po vlogah**.

Vsaka vloga ima svoj blueprint z lastnimi pogledi in predlogami. Skupne funkcije (npr. prijava) so v ločenem `auth` blueprintu. To odraža dejansko strukturo pravic v aplikaciji in omogoča, da pri razvoju vedno delaš znotraj ene mape.

## Posledice

- **Dobro:** Meje med vlogami so jasne že iz strukture map.
- **Dobro:** Iskanje kode je intuitivno – za voznikovo stran odpreš mapo `driver/`.
- **Dobro:** Onemogoča nenamerno klicanje pogledov ene vloge iz druge brez eksplicitnega uvoza.
- **Slabo:** Skupna logika (npr. obrazci, ki jih uporablja več vlog) mora biti skrbno umeščena; sicer lahko pride do podvajanja.
- **Slabo:** Če se kasneje doda nova vloga, je treba ustvariti nov blueprint in poskrbeti za registracijo v aplikaciji.

## Prednosti in slabosti možnosti

### Blueprints po vlogah

- Dobro, ker je poravnava s poslovnimi mejami naravna.
- Dobro, ker je preverjanje pravic enostavno – blueprint je "svoj" za vlogo.
- Slabo, ker skupne komponente (npr. skupni obrazci za več vlog) zahtevajo dodatno mesto.

### En sam blueprint

- Dobro, ker je najmanj datotek.
- Slabo, ker `routes.py` hitro naraste v stotine vrstic in postane nepregleden.

### Blueprints po funkcionalnostih

- Dobro, ker je primerno za projekte z veliko funkcionalnostmi na vlogo.
- Slabo, ker je za ta projekt manj naravna delitev – funkcionalnosti so tesno vezane na vlogo.

### Blueprints po plasteh

- Dobro, ker gre za klasično MVC delitev.
- Slabo, ker se vsaka sprememba ene funkcionalnosti dotakne več map in povečuje kognitivno obremenitev.

## Več informacij

- [Flask Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/)
- Povezano z ADR [0001](0001-use-server-rendered-monolith.md).
