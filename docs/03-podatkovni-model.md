# 03 – Podatkovni model

## Pregled

Podatkovni model Parklja sestavlja 6 med seboj povezanih entitet:
`User`, `Vehicle`, `ParkingLocation`, `ParkingSession`, `Penalty` in
`Payment`. Vse entitete so shranjene v podatkovni bazi CockroachDB in
dostopane prek SQLAlchemy.

## Entitete in glavna polja

### User

Predstavlja vsakega uporabnika sistema – voznika, operaterja ali
administratorja. Vloga je določena s poljem `role`.

- `id` – primarni ključ
- `email` – unikaten, uporablja se za prijavo
- `password_hash` – zgoščeno geslo
- `full_name` – ime in priimek
- `role` – `driver`, `operator` ali `admin`
- `is_blocked` – ali je račun blokiran
- `created_at` – čas registracije

### Vehicle

Vozilo, ki pripada vozniku. Voznik ima lahko več vozil.

- `id` – primarni ključ
- `user_id` – tuji ključ na `User` (lastnik)
- `plate` – registrska tablica, unikatna
- `make` – znamka
- `model` – model
- `type` – tip vozila (za MVP samo `car`)

### ParkingLocation

Posamezno parkirišče v nekem mestu. Vsako parkirišče ima svojega
operaterja in svojo urno ceno.

- `id` – primarni ključ
- `name` – ime parkirišča
- `address` – naslov
- `city` – mesto
- `capacity` – število parkirnih mest
- `hourly_rate` – urna cena v EUR
- `operator_id` – tuji ključ na `User` (operater, ki upravlja to
  parkirišče)
- `is_active` – ali je parkirišče aktivno

### ParkingSession

Osrednja entiteta. Predstavlja eno parkiranje enega vozila na enem
parkirišču.

- `id` – primarni ključ
- `user_id` – tuji ključ na `User` (voznik)
- `vehicle_id` – tuji ključ na `Vehicle`
- `location_id` – tuji ključ na `ParkingLocation`
- `started_at` – čas začetka seje
- `expected_end_at` – predvideni čas zaključka (za prikaz)
- `ended_at` – dejanski čas zaključka (NULL, dokler seja traja)
- `status` – `pending`, `active`, `completed` ali `cancelled`
- `expected_fee` – predvideni znesek ob začetku seje (za prikaz)
- `total_fee` – končni znesek, izračunan ob zaključku
- `is_paid` – ali je seja plačana

### Penalty

Kazen, ki jo operater izda vozilu brez veljavne seje. Kazni se vežejo
na vozilo in na voznika.

- `id` – primarni ključ
- `vehicle_id` – tuji ključ na `Vehicle`
- `user_id` – tuji ključ na `User` (voznik, lastnik vozila)
- `operator_id` – tuji ključ na `User` (operater, ki je kazen izdal)
- `location_id` – tuji ključ na `ParkingLocation`
- `reason` – `no_session`
- `amount` – znesek kazni
- `is_paid` – ali je kazen plačana
- `issued_at` – čas izdaje

### Payment

Ločen zapis o plačilu seje. Za MVP je plačilo vedno simulirano –
voznik samo označi sejo kot plačano, zato entiteta ne vsebuje podatkov
o kartici ali načinu plačila.

- `id` – primarni ključ
- `session_id` – tuji ključ na `ParkingSession`
- `amount` – plačani znesek
- `paid_at` – čas plačila

## Povezave med entitetami

- `User` 1 : N `Vehicle` – voznik ima lahko več vozil.
- `User` 1 : N `ParkingSession` – voznik ima lahko več sej.
- `User` 1 : N `ParkingLocation` – operater upravlja eno parkirišče
  (v modelu je povezava 1:N, ker lahko administrator dodeli operaterja
  tudi več parkiriščem, v MVP pa velja pravilo en operater – eno
  parkirišče).
- `User` 1 : N `Penalty` – kot voznik (prejemnik) in kot operater
  (izdajatelj).
- `Vehicle` 1 : N `ParkingSession`.
- `Vehicle` 1 : N `Penalty`.
- `ParkingLocation` 1 : N `ParkingSession`.
- `ParkingLocation` 1 : N `Penalty`.
- `ParkingSession` 1 : N `Payment` – za MVP ena seja, eno plačilo, v
  modelu pa je povezava 1:N, da ostaja prostor za kasnejše delne
  oziroma večkratne payment-e.

## Osnutek podatkovnega modela

```mermaid
erDiagram
    User ||--o{ Vehicle : owns
    User ||--o{ ParkingSession : drives
    User ||--o{ ParkingLocation : operates
    User ||--o{ Penalty : receives
    User ||--o{ Penalty : issues
    Vehicle ||--o{ ParkingSession : used_in
    Vehicle ||--o{ Penalty : has
    ParkingLocation ||--o{ ParkingSession : hosts
    ParkingLocation ||--o{ Penalty : issued_at
    ParkingSession ||--o{ Payment : paid_by

    User {
        int id PK
        string email
        string password_hash
        string full_name
        string role
        bool is_blocked
        datetime created_at
    }
    Vehicle {
        int id PK
        int user_id FK
        string plate
        string make
        string model
        string type
    }
    ParkingLocation {
        int id PK
        string name
        string address
        string city
        int capacity
        decimal hourly_rate
        int operator_id FK
        bool is_active
    }
    ParkingSession {
        int id PK
        int user_id FK
        int vehicle_id FK
        int location_id FK
        datetime started_at
        datetime expected_end_at
        datetime ended_at
        string status
        decimal expected_fee
        decimal total_fee
        bool is_paid
    }
    Penalty {
        int id PK
        int vehicle_id FK
        int user_id FK
        int operator_id FK
        int location_id FK
        string reason
        decimal amount
        bool is_paid
        datetime issued_at
    }
    Payment {
        int id PK
        int session_id FK
        decimal amount
        datetime paid_at
    }
