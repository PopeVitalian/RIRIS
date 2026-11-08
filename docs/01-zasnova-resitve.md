# 01 – Zasnova rešitve

## Ime rešitve

**AvtoTrg** – spletna platforma za trgovanje z rabljenimi avtomobili v Sloveniji.

## Namen rešitve in problem

Slovenski trg rabljenih avtomobilov je razdrobljen. Kupci brskajo po več portalih hkrati (npr. avto.net, bolha.com, Facebook skupine), kjer kakovost oglasov niha, cene pa so pogosto okvirne. Ko kupec najde zanimiv avto, stik s prodajalcem poteka prek telefona ali e-pošte, brez jasne strukture: ni zapisa o tem, kaj je bilo ponujeno, kdaj in pod kakšnimi pogoji. Prodajalci (predvsem zasebniki) prejemajo ponudbe razpršeno, težko jih je primerjati in pogosto izgubijo sled, katera ponudba je bila sprejeta.

AvtoTrg naslavlja ta problem z enotno platformo, kjer:

- kupec odds **strukturirano ponudbo** na posamezen oglas (znesek + sporočilo),
- prodajalec vidi **vse prejete ponudbe na svoje oglase** na enem mestu,
- ob sprejemu ponudbe sistem **samodejno zavrne preostale** ponudbe in oglas preide v status `rezerviran`,
- po prodaji se oglas zapre v status `prodan`, ponudbe in zgodovina ostanejo sledljivi.

Rešitev ne uvaja posredniških provizij – prodajalec obdrži polno ceno, kupec pa ima vpogled v to, kaj in kdaj je ponudil.

## Ciljni uporabniki

**Kupci rabljenih avtomobilov.** Posamezniki, ki iščejo vozilo zase ali za družino in želijo ponudbo oddati hitro, brez klicev in dogovarjanja prek več kanalov. Zanima jih predvsem: filtriranje po znamki, modelu, gorivu in ceni; jasen pregled lastnih oddanih ponudb in njihovega statusa.

**Prodajalci rabljenih avtomobilov.** Dve podskupini:

- zasebni prodajalci, ki prodajo en ali dva avtomobila na leto;
- avtohiše in manjši trgovci, ki imajo hkrati aktivnih več oglasov in potrebujejo pregled nad prejetimi ponudbami.

Oboji potrebujejo: enostavno objavo oglasa, pregled ponudb na enem mestu, jasno odločitev (sprejmi/zavrni) in status oglasa, ki odraža dejansko stanje (aktiven, rezerviran, prodan).

**Administratorji.** Skrbniki platforme, ki skrbijo za red: blokirajo sumljive uporabnike, odstranjujejo sporne oglase in pregledujejo celotno stanje sistema.

## Kratek opis delovanja

Tipičen potek za kupca:

1. Kupec se registrira in se prijavi.
2. Na domači strani brska po oglasih, uporabi iskanje ali filtre (znamka, model, gorivo, cenovni razpon).
3. Odpre posamezen oglas in vidi vse podatke o vozilu, ceno in prodajalca.
4. Pod oglasom odda ponudbo: vnese znesek in sporočilo (npr. "Ponujam 12.500 €, prevzem v roku tedna dni").
5. Ponudba dobi status `pending`; kupec jo vidi v svoji zgodovini ponudb in jo lahko umakne, dokler je še `pending`.
6. Ko prodajalec ponudbo sprejme, ponudba preide v `accepted`, vse ostale `pending` ponudbe na istem oglasu pa v `rejected`, oglas pa v `rezerviran`.

Tipičen potek za prodajalca:

1. Prodajalec se registrira (pri registraciji izbere vlogo "Prodajalec" ali pa pozneje zahteva nadgradnjo prek gumba "Postani prodajalec"; admin lahko vlogo spremeni tudi ročno).
2. Objavi oglas: znamka, model, letnik, prevoženi kilometri, gorivo, menjalnik, cena, opis.
3. Oglas dobi status `aktivni` in se prikaže na seznamu.
4. Prodajalec spremlja prejete ponudbe – za vsako vidi znesek, sporočilo kupca in čas oddaje.
5. Ponudbo lahko **sprejme** ali **zavrne**. Ob sprejemu sistem samodejno zavrne ostale ponudbe in oglas preide v `rezerviran`.
6. Po zaključeni prodaji prodajalec označi oglas kot `prodan`.

Tipičen potek za administratorja:

- Admin vidi seznam vseh uporabnikov in vseh oglasov.
- Uporabnika lahko blokira (npr. ob sumu na prevaro) in ga pozneje odblokira.
- Oglas lahko blokira ali odstrani.
- Admin ne kupuje in ne prodaja – njegove pravice so omejene na upravljanje platforme.
