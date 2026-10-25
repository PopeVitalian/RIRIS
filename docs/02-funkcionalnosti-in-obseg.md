# 02 – Funkcionalnosti in obseg

## Uporabniške vloge

Voznik (Driver) je končni uporabnik, ki parkira na enem od
parkirišč v sistemu. Registrira se, doda svoja vozila, zažene in
zaključi parkirno sejo ter pregleda svojo zgodovino in kazni. Ne vidi
podatkov drugih voznikov, ne more upravljati parkirišč ali cen in ne
more dostopati do administrativnih funkcij.

Parkirni operater (Parking Operator) je zaposleni na točno enem
parkirišču. Spremlja zasedenost svojega parkirišča, preverja vozila po
registrski tablici, ročno zaključuje seje ob izstopu in izdaja kazni
vozilom brez veljavne seje. Ne vidi drugih parkirišč, ne more
upravljati uporabnikov ali cen.

Lokalni Admin (Local Admin) je skrbnik enega parkirišča oz. mesta. Upravlja eno parkirišče oz. parkirišča enega mesta,
cene teh parkirišč in ročno blokira račune.

Administrator (Admin) je skrbnik celotnega sistema. Upravlja vse uporabnike,
vsa parkirišča in cene, ročno blokira in odblokira račune.

## Predvidene funkcionalnosti

1. **[MVP]** Registracija, prijava in odjava uporabnikov z
   upravljanjem sej.
2. **[MVP]** Nadzorne plošče, prilagojene vlogi (Driver, Operator,
   Admin).
3. Voznik: upravljanje lastnih vozil – dodajanje, urejanje in
   odstranjevanje vozil z registrsko tablico, znamko, modelom in
   tipom.
4. Voznik: pregled parkirišč v sistemu s trenutno zasedenostjo in
   urno ceno.
5. **[MVP]** Voznik zažene parkirno sejo z izbiro vozila in
   predvidenega trajanja; sistem ustvari sejo s statusom `pending`
   in izračuna predvideni znesek.
6. **[MVP]** Voznik zaključi parkirno sejo; sistem izračuna končni
   znesek glede na dejansko trajanje.
7. Voznik: pregled zgodovine lastnih parkirnih sej z zneski in
   statusi.
8. Voznik: označitev plačila seje kot plačano (simulacija).
9. **[MVP]** Operater vidi trenutno zasedenost svojega parkirišča v
   živo.
10. **[MVP]** Operater preveri vozilo po registrski tablici
    (simulacija rampe) in dovoli vstop ali izstop.
11. **[MVP]** Operater izda kazen vozilu brez veljavne seje,
12. **[MVP]** Admin upravlja parkirišča: lokacije, naslove,
    kapacitete in urne cene.
13. Admin upravlja uporabnike: pregled, spreminjanje vlog, ročna
    blokada in odblokada računa.
14. Samodejni izračun parkirnine ob zaključku seje glede na dejansko trajanje, z 15-minutnim tolerančnim pragom.
15. Samodejna blokada računa po 3 neplačanih kaznih in ročna
    odblokada s strani administratorja.

MVP funkcionalnosti so označene z **[MVP]**.

## Kasnejše nadgradnje

1. Voznikove priljubljene lokacije – voznik lahko označi
   parkirišča, ki jih pogosto uporablja, in jih vidi na vrhu
   seznama.
2. Pritožbe na kazni – voznik lahko odda pritožbo na izdano
   kazen, administrator jo pregleda in potrdi ali razveljavi.
3. Izvozi poročil – administrator lahko izvozi poročila
   o zasedenosti in prihodkih za nadaljnjo analizo.
4. Polnilna mesta za električna vozila – posebna oznaka
   parkirnega mesta in ločena tarifa za polnjenje.
5. Mesečne naročnine – možnost rezerviranega parkirnega mesta
   za mesečne naročnike z nižjo ceno.
   - Zemljevid parkirišč in "vizualno" izbiranje parkirišč.

## Out of scope

- Pravi plačilni sistem (Stripe, PayPal, kartično plačevanje)
- Prava ANPR kamera, fizične rampe, senzorji in druga strojna
  oprema
- Native mobilna aplikacija (Android / iOS).
- Integracija z javnim prevozom ali drugimi načini mobilnosti.
- Multi-tenant SaaS (podizvajalci in ločene baze).
