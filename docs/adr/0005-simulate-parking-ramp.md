# 0005 – Simulacija rampe namesto prave strojne opreme

## Status

Sprejeto

## Kontekst in problem

Ena od ključnih funkcionalnosti MVP je preverjanje vozila na rampi in prehod seje iz `pending` v `active`. V resničnem svetu bi to počela ANPR kamera ali RFID bralnik v povezavi s fizično rampo. Prava strojna oprema pa ni na voljo, je draga in je izven obsega predmeta. Potrebujemo način, kako funkcionalnost preizkusiti in demonstrirati brez strojne opreme.

## Odločitveni dejavniki

- Ni stroškov strojne opreme
- Demonstracija toka (vstop/izstop) mora biti mogoča
- Ločitev poslovne logike od specifične strojne opreme
- Enostavno testiranje

## Obravnavane alternative

1. Simulirana rampa kot spletna stran z vnosom tablice
2. Simulacija z vnaprej pripravljenimi testnimi podatki (seed)
3. Prava ANPR kamera (izven obsega)
4. Mobilna aplikacija kot "terminal" (izven obsega)

## Odločitev

Izbrana možnost: **simulirana rampa kot spletna stran z vnosom registrske tablice**.

Operater (ali kdorkoli s pravicami) na ločeni strani vnese tablico in sistem izvede enako logiko, kot bi jo izvedla prava rampa: poišče veljavno sejo, prikaže podatke in omogoči prehod `pending` → `active` ali zaključek seje ob izstopu. S tem je poslovna logika ločena od strojne opreme – kasnejša zamenjava simulacije s pravim ANPR sistemom bi zahtevala le zamenjavo vhodne točke, ne pa spremembe v poslovni logiki.

## Posledice

- **Dobro:** Ni stroškov strojne opreme in ni odvisnosti od fizičnega okolja.
- **Dobro:** Demonstracija in testiranje sta trivialna.
- **Dobro:** Poslovna logika ostaja ločena od specifičnega vmesnika rampe.
- **Slabo:** Simulacija ne zajema resničnih časovnih omejitev (npr. zakasnitve odziva kamere) in ne odkriva morebitnih težav v realnem okolju.
- **Slabo:** Uporabniška izkušnja operaterja se razlikuje od resničnega terminala na rampi.

## Prednosti in slabosti možnosti

### Simulirana rampa

- Dobro, ker je poceni in ponovljivo.
- Dobro, ker je primerno za demonstracijo in ocenjevanje.
- Slabo, ker manjka realističnost.

### Seed podatki

- Dobro, ker je najhitrejše.
- Slabo, ker ne omogoča interaktivne demonstracije toka.

### Prava ANPR kamera

- Dobro, ker je realistično.
- Slabo, ker je izven obsega predmeta in proračuna.

### Mobilna aplikacija kot terminal

- Dobro, ker je prenosno.
- Slabo, ker zahteva razvoj mobilne aplikacije, kar je prav tako izven obsega.

## Več informacij

- Povezano z ADR [0001](0001-use-server-rendered-monolith.md).
- Funkcionalnost F-10 v [02-funkcionalnosti-in-obseg.md](../02-funkcionalnosti-in-obseg.md).