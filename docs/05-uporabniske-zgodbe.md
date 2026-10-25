# 05 – Uporabniške zgodbe

## Pregled

| Oznaka | Funkcionalnost (02) | Vloga | Kratki opis |
|--------|---------------------|-------|-------------|
| US-01  | F-01 Registracija, prijava, odjava | Gost | Registracija računa |
| US-02  | F-01 | Vse vloge | Prijava in odjava |
| US-03  | F-02 Nadzorne plošče po vlogi | Voznik | Pregled lastne plošče |
| US-04  | F-03 Upravljanje vozil | Voznik | Dodajanje/urejanje/brisanje vozil |
| US-05  | F-04 Pregled parkirišč | Voznik | Seznam parkirišč s ceno in zasedenostjo |
| US-06  | F-05 Začetek parkirne seje | Voznik | Nova seja s statusom `pending` |
| US-07  | F-06 + F-14 Zaključek in izračun | Voznik | Zaključek seje z izračunom parkirnine |
| US-08  | F-07 Zgodovina sej | Voznik | Pregled preteklih sej |
| US-09  | F-08 Označitev plačila | Voznik | Simulirano plačilo seje |
| US-10  | F-09 Zasedenost parkirišča | Operater | Pregled zasedenosti v živo |
| US-11  | F-10 Preverjanje tablice | Operater | Simulacija rampe |
| US-12  | F-11 Izdaja kazni | Operater | Kazen za vozilo brez seje |
| US-13  | F-12 Upravljanje parkirišč | Admin | CRUD parkirišč in cen |
| US-14  | F-13 Upravljanje uporabnikov | Admin | Vloge, blokada, odblokada |
| US-15  | F-15 Samodejna blokada računa | Sistem | Blokada po 3 neplačanih kaznih |

---

### US-01 — Registracija

**Funkcionalnost:** F-01 Registracija, prijava in odjava
**Vloga:** Gost (bodoči voznik)

Kot gost želim ustvariti uporabniški račun, da lahko uporabljam Parkelj.

**Acceptance criteria:**
1. Obrazec vsebuje polja e-pošta, geslo in potrditev gesla.
2. Sistem zavrne neveljaven e-poštni naslov in prikaže sporočilo o napaki.
3. Geslo mora imeti vsaj 8 znakov; sicer se registracija zavrne.
4. Ob uspešni registraciji se uporabnik preusmeri na prijavno stran.
5. Če e-pošta že obstaja, se prikaže sporočilo "Račun s to e-pošto že obstaja."

---

### US-02 — Prijava in odjava

**Funkcionalnost:** F-01
**Vloga:** Voznik / Operater / Admin

Kot registrirani uporabnik želim se prijaviti in odjaviti, da varno dostopam do svojega računa.

**Acceptance criteria:**
1. Prijavni obrazec vsebuje e-pošto in geslo.
2. Ob pravilnih podatkih se prikaže nadzorna plošča glede na vlogo.
3. Ob napačnih podatkih se prikaže splošno sporočilo "Napačna e-pošta ali geslo."
4. Gumb "Odjava" prekine sejo in preusmeri na prijavno stran.
5. Zaščitene strani brez prijave preusmerijo na prijavno stran.

---

### US-03 — Nadzorna plošča voznika

**Funkcionalnost:** F-02 Nadzorne plošče po vlogi
**Vloga:** Voznik

Kot voznik želim na enem mestu videti svoja vozila, aktivno sejo in bližnjice, da hitro ukrepam.

**Acceptance criteria:**
1. Plošča prikaže seznam mojih vozil.
2. Če obstaja aktivna seja, so prikazani parkirišče, začetek in predvideni znesek.
3. Prikazani sta povezavi "Začni parkiranje" in "Moja zgodovina".
4. Podatki drugih voznikov niso vidni.

---

### US-04 — Upravljanje vozil

**Funkcionalnost:** F-03 Upravljanje vozil
**Vloga:** Voznik

Kot voznik želim dodajati, urejati in brisati svoja vozila, da so podatki vedno pravilni.

**Acceptance criteria:**
1. Obrazec vsebuje polja tablica, znamka, model in tip.
2. Registrska tablica je unikatna; podvojen vnos je zavrnjen s sporočilom.
3. Voznik lahko ureja in briše le svoja vozila.
4. Ob brisanju se prikaže potrditveno okno.
5. Po uspešni spremembi se seznam vozil takoj osveži.

---

### US-05 — Pregled parkirišč

**Funkcionalnost:** F-04 Pregled parkirišč
**Vloga:** Voznik

Kot voznik želim videti seznam parkirišč z zasedenostjo in urno ceno, da izberem najbolj ustrezno.

**Acceptance criteria:**
1. Seznam prikaže ime, mesto, naslov, urno ceno in razmerje zasedenih/prostih mest.
2. Neaktivna parkirišča niso prikazana.
3. Omogočen je filter po mestu.
4. Klik na parkirišče odpre podrobnost z gumbom "Začni parkiranje".

---

### US-06 — Začetek parkirne seje

**Funkcionalnost:** F-05 Začetek parkirne seje
**Vloga:** Voznik

Kot voznik želim začeti parkirno sejo z izbiro vozila in predvidenega trajanja, da si zagotovim veljavno parkiranje.

**Acceptance criteria:**
1. Obrazec omogoča izbiro enega od mojih vozil in vnos predvidenega trajanja v urah.
2. Sistem izračuna predvideni znesek kot zmnožek trajanja in urne cene ter ga prikaže pred potrditvijo.
3. Ob potrditvi se ustvari seja s statusom `pending` in prikaže potrditev.
4. Voznik ne more začeti nove seje za isto vozilo, dokler prejšnja ni zaključena.

---

### US-07 — Zaključek seje in izračun parkirnine

**Funkcionalnost:** F-06 Zaključek seje + F-14 Samodejni izračun
**Vloga:** Voznik

Kot voznik želim zaključiti sejo, da se obračuna dejanska parkirnina.

**Acceptance criteria:**
1. Ob zaključku sistem izračuna trajanje od `started_at` do trenutka zaključka.
2. Prvih 15 minut prekoračitve se ne obračuna (tolerančni prag).
3. Končni znesek se zapiše v `total_fee`, seja dobi status `completed`.
4. Če je dejansko trajanje krajše od predvidenega, se obračuna le dejansko trajanje.
5. Voznik vidi povzetek z začetkom, koncem in končnim zneskom.

---

### US-08 — Zgodovina sej

**Funkcionalnost:** F-07 Zgodovina sej
**Vloga:** Voznik

Kot voznik želim pregledati svoje pretekle seje, da imam pregled nad porabo in plačili.

**Acceptance criteria:**
1. Seznam prikaže datum, parkirišče, trajanje, znesek in status plačila.
2. Seje so razvrščene od najnovejše do najstarejše.
3. Voznik vidi samo svoje seje.
4. Omogočen je filter po datumu (od–do).

---

### US-09 — Označitev plačila

**Funkcionalnost:** F-08 Označitev plačila (simulacija)
**Vloga:** Voznik

Kot voznik želim označiti sejo kot plačano, da zaključim postopek (simulirano plačilo).

**Acceptance criteria:**
1. Na zaključeni seji je viden gumb "Označi kot plačano".
2. Ob kliku se ustvari zapis v `Payment` z zneskom in časom plačila.
3. Seja dobi `is_paid = true` in gumb se skrije.
4. Plačila ni mogoče označiti za tujo sejo.

---

### US-10 — Operater: zasedenost parkirišča

**Funkcionalnost:** F-09 Zasedenost parkirišča
**Vloga:** Operater

Kot operater želim videti trenutno zasedenost svojega parkirišča, da spremljam stanje na terenu.

**Acceptance criteria:**
1. Plošča prikaže število aktivnih sej in število prostih mest (kapaciteta − aktivne seje).
2. Prikaže se seznam aktivnih sej s tablico in časom začetka.
3. Operater vidi samo svoje parkirišče.
4. Podatki se osvežijo ob vsakem obisku strani.

---

### US-11 — Operater: preverjanje tablice

**Funkcionalnost:** F-10 Preverjanje vozila (simulacija rampe)
**Vloga:** Operater

Kot operater želim preveriti vozilo po registrski tablici, da dovolim vstop ali izstop.

**Acceptance criteria:**
1. Obrazec sprejme registrsko tablico.
2. Če obstaja veljavna seja (`pending` ali `active`), sistem prikaže podatke in gumb "Dovoli vstop/izstop".
3. Če seje ni, sistem prikaže opozorilo in ponudi izdajo kazni.
4. Ob potrditvi vstopa seja preide iz `pending` v `active`.
5. Ob potrditvi izstopa se seja zaključi po pravilih US-07.

---

### US-12 — Operater: izdaja kazni

**Funkcionalnost:** F-11 Izdaja kazni
**Vloga:** Operater

Kot operater želim izdati kazen vozilu brez veljavne seje, da sankcioniram nepravilno parkiranje.

**Acceptance criteria:**
1. Kazen se lahko izda le, če vozilo nima veljavne seje na tem parkirišču.
2. Obrazec vsebuje tablico, razlog (`no_session`) in znesek kazni.
3. Kazen se zabeleži v `Penalty` skupaj z operaterjem in lokacijo.
4. Vozniku se kazen prikaže v njegovem pregledu kazni.
5. Operater ne more izdati kazni za tuje parkirišče.

---

### US-13 — Admin: upravljanje parkirišč

**Funkcionalnost:** F-12 Upravljanje parkirišč
**Vloga:** Admin

Kot admin želim upravljati parkirišča, da so lokacije, kapacitete in cene v sistemu pravilne.

**Acceptance criteria:**
1. Admin lahko doda novo parkirišče z imenom, naslovom, mestom, kapaciteto in urno ceno.
2. Admin lahko ureja in deaktivira obstoječe parkirišče.
3. Urna cena mora biti večja od 0; drugače se prikaže napaka.
4. Kapaciteta mora biti celo število večje od 0.
5. Neaktivno parkirišče se ne prikaže voznikom v pregledu (US-05).

---

### US-14 — Admin: upravljanje uporabnikov

**Funkcionalnost:** F-13 Upravljanje uporabnikov
**Vloga:** Admin

Kot admin želim pregledovati uporabnike ter upravljati njihove vloge in blokade, da ohranjam red v sistemu.

**Acceptance criteria:**
1. Admin vidi seznam uporabnikov z e-pošto, imenom, vlogo in stanjem blokade.
2. Admin lahko spremeni vlogo uporabnika (driver / operator / admin).
3. Admin lahko ročno blokira in odblokira račun.
4. Blokiran uporabnik se ne more prijaviti; pri prijavi se prikaže sporočilo o blokadi.
5. Admin ne more blokirati samega sebe.

---

### US-15 — Samodejna blokada po 3 neplačanih kaznih

**Funkcionalnost:** F-15 Samodejna blokada računa
**Vloga:** Sistem (v ozadju, posledica US-12)

Kot sistem želim samodejno blokirati voznika po 3 neplačanih kaznih, da se zmanjša ponavljanje kršitev.

**Acceptance criteria:**
1. Ob izdaji nove kazni sistem prešteje neplačane kazni voznika (`is_paid = false`).
2. Ko števec doseže 3, se `User.is_blocked` nastavi na `true`.
3. Blokiran voznik ne more začeti nove parkirne seje (zavrnitev na US-06).
4. Admin vidi oznako blokade na seznamu uporabnikov (US-14).
5. Blokada se odpravi le z ročno odblokado s strani admina, ne samodejno ob plačilu.
