# 05 – Uporabniške zgodbe

## Pregled

| Oznaka | Funkcionalnost (02) | Vloga | Kratki opis |
|--------|---------------------|-------|-------------|
| US-01 | F-01 Registracija, prijava, odjava | Gost | Registracija računa |
| US-02 | F-01 | Vse vloge | Prijava in odjava |
| US-03 | F-02 Nadzorne plošče po vlogi | Vse vloge | Pregled lastne plošče |
| US-04 | F-03 Iskanje in filtriranje | Kupec | Iskanje oglasov |
| US-05 | F-04 Oddaja ponudbe | Kupec | Oddaja ponudbe na oglas |
| US-06 | F-05 Pregled in umik ponudb | Kupec | Upravljanje lastnih ponudb |
| US-07 | F-06 Zgodovina ponudb | Kupec | Pregled vseh oddanih ponudb |
| US-08 | F-07 Upravljanje oglasov | Prodajalec | Objava/urejanje/brisanje oglasov |
| US-09 | F-08 Pregled prejetih ponudb | Prodajalec | Seznam ponudb na svoje oglase |
| US-10 | F-08 + F-09 Sprejem/zavrnitev z auto-reject | Prodajalec | Odločitev o ponudbi |
| US-11 | F-09 Življenjski cikel oglasa | Prodajalec | Rezerviran → prodan |
| US-12 | F-10 Statistike prodajalca | Prodajalec | Pregled števcev |
| US-13 | F-11 Admin pregled | Admin | Pregled uporabnikov in oglasov |
| US-14 | F-12 Blokade in vloge | Admin | Blokada uporabnikov/oglasov |
| US-15 | F-13 JSON API | Javno | Strojni dostop do oglasov |

---

### US-01 — Registracija

**Funkcionalnost:** F-01 Registracija, prijava in odjava
**Vloga:** Gost (bodoči kupec ali prodajalec)

Kot gost želim ustvariti uporabniški račun, da lahko uporabljam AvtoTrg.

**Sprejemni kriteriji:**

1. Obrazec vsebuje polja: ime, e-pošta, geslo, potrditev gesla, kraj in izbiro vloge (`kupec` / `prodajalec`).
2. Sistem zavrne neveljaven e-poštni naslov in prikaže sporočilo o napaki.
3. Geslo mora imeti vsaj 8 znakov; sicer se registracija zavrne.
4. Ob uspešni registraciji se uporabnik preusmeri na prijavno stran.
5. Če e-pošta že obstaja, se prikaže sporočilo "Račun s to e-pošto že obstaja."

---

### US-02 — Prijava in odjava

**Funkcionalnost:** F-01
**Vloga:** Kupec / Prodajalec / Admin

Kot registrirani uporabnik želim se prijaviti in odjaviti, da varno dostopam do svojega računa.

**Sprejemni kriteriji:**

1. Prijavni obrazec vsebuje e-pošto in geslo.
2. Ob pravilnih podatkih se prikaže nadzorna plošča glede na vlogo.
3. Ob napačnih podatkih se prikaže splošno sporočilo "Napačna e-pošta ali geslo."
4. Blokiran uporabnik se ne more prijaviti; prikaže se sporočilo "Vaš račun je blokiran."
5. Gumb "Odjava" prekine sejo in preusmeri na prijavno stran.

---

### US-03 — Nadzorna plošča

**Funkcionalnost:** F-02 Nadzorne plošče po vlogi
**Vloga:** Vse vloge

Kot prijavljeni uporabnik želim na enem mestu videti povzetek svojega dela, da hitro ukrepam.

**Sprejemni kriteriji:**

1. Kupec vidi seznam svojih zadnjih oddanih ponudb in bližnjico "Brskaj oglase".
2. Prodajalec vidi seznam svojih aktivnih oglasov in število novih ponudb v zadnjih 7 dneh.
3. Admin vidi število uporabnikov, oglasov in ponudb v sistemu.
4. Podatki drugih uporabnikov niso vidni.

---

### US-04 — Iskanje in filtriranje oglasov

**Funkcionalnost:** F-03 Iskanje in filtriranje
**Vloga:** Kupec

Kot kupec želim filtrirati oglase po znamki, modelu, gorivu in ceni, da najdem ustrezen avto.

**Sprejemni kriteriji:**

1. Iskalno polje omogoča iskanje po znamki in modelu (delno ujemanje, neobčutljivo na velikost črk).
2. Filtri omogočajo izbiro goriva in cenovnega razpona (min–max).
3. Rezultati so razvrščeni od najnovejših do najstarejših, s paginacijo po 25 na stran.
4. Neaktivni in blokirani oglasi niso prikazani kupcu.
5. Filter in iskanje se ohranita ob prehodu med stranmi.

---

### US-05 — Oddaja ponudbe

**Funkcionalnost:** F-04 Oddaja ponudbe
**Vloga:** Kupec

Kot kupec želim oddati ponudbo na oglas z zneskom in sporočilom, da prodajalcu jasno sporočim svojo namero.

**Sprejemni kriteriji:**

1. Na strani oglasa je obrazec z polji: znesek (EUR) in sporočilo.
2. Znesek mora biti pozitivno število; drugače se prikaže napaka.
3. Kupec ne more oddati ponudbe na lasten oglas.
4. Kupec ne more oddati ponudbe na oglas, ki ni v statusu `aktivni`.
5. Po uspešni oddaji ponudba dobi status `pending`, kupec pa vidi potrditev in povezavo na svojo zgodovino ponudb.

---

### US-06 — Pregled in umik lastnih ponudb

**Funkcionalnost:** F-05 Pregled in umik ponudb
**Vloga:** Kupec

Kot kupec želim videti svoje ponudbe in jih umakniti, dokler niso odločene, da ohranim nadzor.

**Sprejemni kriteriji:**

1. Kupec vidi seznam svojih ponudb z oglasom, zneskom, statusom in časom oddaje.
2. Ponudbo v statusu `pending` lahko kupec umakne (status → `withdrawn`, zabeleži se `decided_at`).
3. Ponudb v statusih `accepted` in `rejected` ni mogoče umakniti.
4. Kupec vidi samo svoje ponudbe.

---

### US-07 — Zgodovina ponudb

**Funkcionalnost:** F-06 Zgodovina ponudb
**Vloga:** Kupec

Kot kupec želim pregledati vse pretekle ponudbe, da imam evidenco svojih aktivnosti.

**Sprejemni kriteriji:**

1. Seznam prikaže vse ponudbe (v vseh statusih) od najnovejše do najstarejše.
2. Za vsako ponudbo so prikazani: oglas, znesek, status, čas oddaje in (če je odločena) čas odločitve.
3. Omogočen je filter po statusu.
4. Kupec vidi samo svoje ponudbe.

---

### US-08 — Upravljanje lastnih oglasov

**Funkcionalnost:** F-07 Upravljanje oglasov
**Vloga:** Prodajalec

Kot prodajalec želim dodajati, urejati in brisati svoje oglase, da so podatki pravilni in ažurni.

**Sprejemni kriteriji:**

1. Obrazec vsebuje polja: znamka, model, letnik, kilometri, gorivo, menjalnik, cena, opis.
2. Letnik mora biti med 1950 in tekočim letom + 1.
3. Cena mora biti pozitivno število; kilometri morajo biti nenegativni.
4. Prodajalec lahko ureja in briše le svoje oglase.
5. Ob brisanju oglasa se kaskadno izbrišejo vse ponudbe na ta oglas.
6. Oglasa v statusu `prodan` ni mogoče urejati, le pregledati.

---

### US-09 — Pregled prejetih ponudb

**Funkcionalnost:** F-08 Pregled prejetih ponudb
**Vloga:** Prodajalec

Kot prodajalec želim videti vse ponudbe na svoje oglase, da se lahko odločim.

**Sprejemni kriteriji:**

1. Prodajalec vidi seznam ponudb, grupiran po oglasih.
2. Za vsako ponudbo so prikazani: kupec (ime), znesek, sporočilo, čas oddaje in status.
3. Ponudbe v statusu `pending` so vizualno ločene.
4. Prodajalec vidi samo ponudbe na svoje oglase.

---

### US-10 — Sprejem ali zavrnitev ponudbe (z auto-reject)

**Funkcionalnost:** F-08 + F-09
**Vloga:** Prodajalec

Kot prodajalec želim sprejeti eno ponudbo in s tem samodejno zavrniti ostale, da se jasno zaključi pogajanje.

**Sprejemni kriteriji:**

1. Ob sprejemu ponudbe se ta prestavi v `accepted`, zabeleži se `decided_at`.
2. Vsi ostali `pending` ponudbe na istem oglasu se v isti transakciji prestavijo v `rejected`.
3. Oglas se prestavi v status `rezerviran`.
4. Ob zavrnitvi posamezne ponudbe se ta prestavi v `rejected`, oglas ostane `aktivni`.
5. Ponudbe, ki niso več `pending`, ni mogoče ponovno odločiti.
6. Vsi trije koraki (sprejem, avto-zavrnitev, prehod oglasa) se izvedejo atomarno v eni transakciji.

---

### US-11 — Življenjski cikel oglasa

**Funkcionalnost:** F-09 Življenjski cikel
**Vloga:** Prodajalec

Kot prodajalec želim, da oglas samodejno prehaja med statusi, da odraža dejansko stanje.

**Sprejemni kriteriji:**

1. Nov oglas dobi status `aktivni`.
2. Ob sprejemu ponudbe oglas preide v `rezerviran`.
3. Prodajalec lahko oglas v `rezerviran` označi kot `prodan`.
4. Oglasa v `prodan` ni mogoče vrniti v prejšnje stanje brez admina.
5. Admin lahko oglas kadarkoli blokira (status → `blokiran`).

---

### US-12 — Statistike prodajalca

**Funkcionalnost:** F-10 Statistike
**Vloga:** Prodajalec

Kot prodajalec želim videti število aktivnih oglasov in prejetih ponudb, da spremljam uspešnost.

**Sprejemni kriteriji:**

1. Plošča prikaže število aktivnih oglasov (status `aktivni`).
2. Plošča prikaže število prejetih ponudb v zadnjih 30 dneh (vsi statusi).
3. Plošča prikaže število sprejetih ponudb v zadnjih 30 dneh.
4. Podatki se osvežijo ob vsakem obisku strani.

---

### US-13 — Admin: pregled uporabnikov in oglasov

**Funkcionalnost:** F-11 Admin pregled
**Vloga:** Admin

Kot admin želim videti seznam vseh uporabnikov in oglasov, da imam nadzor nad sistemom.

**Sprejemni kriteriji:**

1. Admin vidi seznam uporabnikov z e-pošto, imenom, vlogo, stanjem blokade in datumom registracije.
2. Admin vidi seznam vseh oglasov (tudi blokiranih in prodanih) z osnovnimi podatki.
3. Seznama omogočata paginacijo.
4. Uporabnik lahko poišče po e-pošti, oglas po znamki/modelu.

---

### US-14 — Admin: blokade in vloge

**Funkcionalnost:** F-12 Blokade in vloge
**Vloga:** Admin

Kot admin želim blokirati uporabnike in oglase ter ročno spreminjati vloge, da vzdržujem red.

**Sprejemni kriteriji:**

1. Admin lahko blokira in odblokira uporabnika (`users.is_blocked`).
2. Blokiran uporabnik se ne more prijaviti in ne more oddati novih ponudb.
3. Admin lahko blokira ali odstrani oglas.
4. Admin lahko uporabniku ročno spremeni vlogo (`buyer` → `seller`, `seller` → `admin`, itd.).
5. Admin ne more blokirati drugega administratorja in ne more spremeniti lastne vloge.

---

### US-15 — Javni JSON API

**Funkcionalnost:** F-13 JSON API
**Vloga:** Javno (strojni dostop)

Kot razvijalec tretjega sistema želim pridobiti seznam aktivnih oglasov v JSON obliki, da jih prikažem na svoji strani.

**Sprejemni kriteriji:**

1. `GET /api/listings` vrne JSON s seznamom aktivnih oglasov.
2. Podprti so parametri `make`, `limit` (1–100) in `offset`.
3. Vsak oglas vsebuje: id, make, model, year, mileage_km, fuel, transmission, price_eur, seller (ime), created_at.
4. Blokirani in prodani oglasi niso vključeni.
5. Odgovor je vedno v obliki `{"count": N, "listings": [...]}`.
