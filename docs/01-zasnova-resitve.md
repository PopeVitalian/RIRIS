# 01 – Zasnova rešitve

## Ime rešitve

**Parkelj** – spletna platforma za upravljanje parkirišč v več mestih.

## Namen rešitve in problem

V Sloveniji obstaja več ločenih aplikacij in sistemov za plačevanje
parkirnin. Vsako mesto, občina ali zasebni upravljavec parkirišč ima
pogosto svojo aplikacijo, svoj račun in svoj način plačila. Za voznika
to pomeni, da mora imeti nameščenih več aplikacij, več uporabniških
računov in več načinov plačila, tudi če parkira samo občasno v različnih
mestih.

Rešitve, ki poskušajo ta problem poenotiti (npr. EasyPark), to storijo
tako, da uvedejo svoje storitvene tarife in provizije, ki jih
upravljavcem parkirišč in posledično voznikom zaračunajo povrhu
parkirnine. Vozniki tako plačujejo več, upravljavci pa so vezani na
posrednika.

Parkelj naslavlja ta problem z enotno spletno platformo za več mest
in več upravljavcev hkrati.

## Ciljni uporabniki

Parkelj je namenjen trem skupinam ljudi.

Prva skupina so vozniki, ki parkirajo v več različnih mestih in
želijo za vsa parkiranja uporabiti eno aplikacijo, en račun in en
način plačila. To so pogosto dnevni migranti, študenti, dostavljavci
in občasni obiskovalci mest, ki jih moti, da morajo za vsako mesto
posebej iskati aplikacijo in ustvarjati nov račun.

Druga skupina so upravljavci parkirišč, občine, zasebna podjetja
in posamezna parkirišča, ki želijo ponuditi svoje storitve v skupni
platformi, brez da bi plačevali provizije posrednikom in brez da bi
razvijali svojo aplikacijo. Sem spadajo tako upravljavci javnih
parkirišč kot tudi upravljavci zasebnih garaž in parkirišč ob
trgovskih centrih.

Tretja skupina so operaterji na terenu, ki fizično nadzorujejo
parkirišča in potrebujejo preprosto orodje za preverjanje veljavnosti
parkiranja, izdajanje kazni in spremljanje zasedenosti v živo.

## Kratek opis delovanja

Tipičen potek uporabe za voznika:

1. Voznik se registrira in doda svoje vozilo (registrska tablica,
   znamka, model, tip).
2. Ob prihodu na parkirišče v brskalniku zažene novo parkirno sejo:
   izbere vozilo in vnese predvideno trajanje parkiranja (npr. 2 uri).
3. Sistem ustvari parkirno sejo s statusom `pending` in izračuna
   predvideni znesek glede na urno ceno parkirišča.
4. Na rampi (simuliran terminal) operater ali terminal preveri
   registrsko tablico. Če veljavna seja obstaja, se rampa odpre in seja
   preide v status `active`.
5. Med parkiranjem operater obhodi parkirišče in preveri
   posamezna vozila. Če vozilo nima veljavne seje, operater izda kazen.
6. Ob odhodu voznik zaključi sejo v aplikaciji, ali pa terminal na
   rampi samodejno zazna izstop in sejo zaključi. Če je predvideni čas
   že potekel, se obračuna dodatna parkirnina za prekoračitev, pri čemer velja 15-minutni tolerančni prag.
7. Sistem izračuna končni znesek in ustvari zapis o plačilu. Voznik
   plačilo označi kot plačano.
8. Če voznik nabere tri kazni, se njegov račun samodejno
   blokira. Administrator ga lahko ročno odblokira.

Tipičen potek za operaterja in administratorja:

- Operater vidi samo svoje parkirišče: zasedenost, aktivne seje in
  seznam vozil. Lahko izdaja kazni in ročno preverja tablice.
- Administrator vidi vsa parkirišča v vseh mestih, upravlja cene,
  kapacitete, uporabnike in vloge.
