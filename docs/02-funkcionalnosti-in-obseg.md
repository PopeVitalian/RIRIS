# 02 – Funkcionalnosti in obseg

## Uporabniške vloge

**Kupec (Buyer).** Končni uporabnik, ki išče in kupuje rabljen avtomobil.

- **Kaj lahko počne:** brska po oglasih, uporablja iskanje in filtre (znamka, model, gorivo, cenovni razpon), odpira detajle oglasov, oddaja ponudbe, spremlja status svojih ponudb in jih umakne, dokler so v statusu `pending`, pregleduje svojo zgodovino ponudb.
- **Česa ne more:** ne more ustvarjati oglasov, ne more videti ponudb drugih kupcev, ne more upravljati uporabnikov, ne more blokirati oglasov, ne more spreminjati statusa oglasa. Vlogo kupca dobi vsak nov registrirani uporabnik privzeto.

**Prodajalec (Seller).** Uporabnik, ki objavlja avtomobile naprodaj.

- **Kaj lahko počne:** objavi nov oglas, ureja in briše svoje oglase, vidi vse prejete ponudbe na svoje oglase, sprejme ali zavrne posamezno ponudbo, označi oglas kot `rezerviran` ali `prodan`.
- **Česa ne more:** ne vidi ponudb na tuje oglase, ne vidi seznama vseh uporabnikov, ne more blokirati uporabnikov, ne more upravljati tujih oglasov. Vlogo prodajalca dobi uporabnik ob registraciji (izbere vlogo "Prodajalec") ali prek zahteve za nadgradnjo iz vloge kupca; admin lahko vlogo spremeni ročno.

**Administrator (Admin).** Skrbnik platforme.

- **Kaj lahko počne:** vidi vse uporabnike in vse oglase, uporabnika blokira in odblokira, oglas blokira ali odstrani, uporabniku ročno spremeni vlogo.
- **Česa ne more:** ne more kupovati ali prodajati (nima lastnih oglasov ali ponudb), ne more blokirati drugega administratorja, ne more spremeniti lastne vloge.

## Predvidene funkcionalnosti

1. **[MVP]** Registracija, prijava in odjava z upravljanjem sej.
2. **[MVP]** Nadzorne plošče, prilagojene vlogi (kupec, prodajalec, admin).
3. **[MVP]** Kupec: iskanje in filtriranje oglasov po znamki, modelu, gorivu in cenovnem razponu.
4. **[MVP]** Kupec: oddaja strukturirane ponudbe na posamezen oglas (znesek + sporočilo).
5. Kupec: pregled lastnih oddanih ponudb in umik ponudbe v statusu `pending`.
6. Kupec: zgodovina vseh ponudb z jasnim statusom (`pending`, `accepted`, `rejected`, `withdrawn`).
7. **[MVP]** Prodajalec: objava, urejanje in brisanje lastnih oglasov.
8. **[MVP]** Prodajalec: pregled prejetih ponudb, sprejem ali zavrnitev posamezne ponudbe; **samodejna zavrnitev preostalih `pending` ponudb ob sprejemu**.
9. **[MVP]** Prodajalec: prehod oglasa skozi stanja `aktivni` → `rezerviran` (ob sprejemu ponudbe) → `prodan` (ob prodaji).
10. Prodajalec: statistike – število aktivnih oglasov in število prejetih ponudb v zadnjih 30 dneh.
11. Admin: pregled vseh uporabnikov in vseh oglasov (tudi blokiranih).
12. Admin: blokada in odblokada uporabnikov, blokada in odstranitev oglasov, ročna sprememba vloge uporabnika.
13. Javni JSON API za seznam aktivnih oglasov (`/api/listings`) – za strojni dostop in preverjanje.
14. Vsi: javni profil prodajalca z vsemi njegovimi aktivnimi oglasi.
15. Prodajalec: oznaka "avtohiša" na uporabniškem računu (vpliva na prikaz v oglasih).

MVP funkcionalnosti so označene z **[MVP]** – sedem jih je. Vsaj tri so **domensko specifične** za avtomobilski trg in ne le CRUD: **#4 (strukturirana ponudba)**, **#8 (sprejem ponudbe z auto-reject)** in **#9 (življenjski cikel oglasa skozi rezerviran/prodan)**.

## Kasnejše nadgradnje

1. **Priljubljeni oglasi (watchlist).** Kupec označi oglase, ki jih spremlja, in dobi seznam "moji priljubljeni".
2. **Pritožbe na blokade.** Blokiran uporabnik odda pritožbo; admin jo pregleda in potrdi ali razveljavi.
3. **Izvozi poročil.** Admin izvozi CSV/JSON poročilo o uporabnikih, oglasih in ponudbah.
4. **Nalaganje fotografij oglasov.** Prodajalec naloži do N fotografij na oglas.
5. **Mesečne naročnine za avtohiše.** Premium oglasi z večjo vidnostjo in dodatnimi statistikami.
6. **Zemljevid s kraji prodajalcev.** Prikaz oglasov na zemljevidu (Leaflet ali MapLibre).
7. **Ocene in mnenja o prodajalcih.** Kupec po zaključeni transakciji oceni prodajalca; prikaz povprečne ocene.

## Out of scope

Ta projekt **ne bo** vseboval:

- pravega plačilnega sistema (Stripe, PayPal, kartično plačevanje) – vse transakcije so simulirane;
- realnočasovnega klepeta med kupcem in prodajalcem;
- native mobilne aplikacije (Android / iOS);
- e-poštnih ali SMS obvestil;
- multi-tenant SaaS (ločene baze za vsako avtohišo).
