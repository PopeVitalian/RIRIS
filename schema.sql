-- =========================================================
-- AvtoTrg – shema (PostgreSQL)
-- Tri povezane entitete:
--   users    – kupci, prodajalci, admini
--   listings – oglasi (pripadajo prodajalcu)
--   offers   – ponudbe (kupec -> oglas)
-- Zagon:
--   docker exec -i pts-postgres psql -U avtotrg -d avtotrg_db < schema.sql
-- =========================================================

-- Enumi (idempotentno).
DO $$ BEGIN
    CREATE TYPE fuel_type AS ENUM ('bencin', 'dizel', 'hibrid', 'električni', 'plin');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE transmission_type AS ENUM ('ročni', 'avtomatski');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('buyer', 'seller', 'admin');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE listing_status AS ENUM ('aktivni', 'rezerviran', 'prodan', 'blokiran');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE offer_status AS ENUM ('pending', 'accepted', 'rejected', 'withdrawn');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- users: ena vrstica na uporabnika. Vloga določa pravice.
CREATE TABLE IF NOT EXISTS users (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name     VARCHAR(120) NOT NULL,
    phone         VARCHAR(30),
    city          VARCHAR(60)  NOT NULL,
    role          user_role    NOT NULL DEFAULT 'buyer',
    is_dealer     BOOLEAN      NOT NULL DEFAULT FALSE,
    is_blocked    BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_role ON users (role);

-- listings: oglas. Pripada natanko enemu prodajalcu.
CREATE TABLE IF NOT EXISTS listings (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    make         VARCHAR(50) NOT NULL,
    model        VARCHAR(60) NOT NULL,
    year         INTEGER NOT NULL,
    mileage_km   INTEGER NOT NULL,
    fuel         fuel_type         NOT NULL,
    transmission transmission_type NOT NULL,
    price_eur    NUMERIC(10,2) NOT NULL,
    status       listing_status NOT NULL DEFAULT 'aktivni',
    description  TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT year_sane             CHECK (year BETWEEN 1950 AND 2100),
    CONSTRAINT price_positive        CHECK (price_eur > 0),
    CONSTRAINT mileage_nonneg        CHECK (mileage_km >= 0),
    CONSTRAINT updated_after_created CHECK (updated_at >= created_at)
);

CREATE INDEX IF NOT EXISTS idx_listings_seller ON listings (seller_id);
CREATE INDEX IF NOT EXISTS idx_listings_make   ON listings (make);
CREATE INDEX IF NOT EXISTS idx_listings_active
    ON listings (created_at DESC)
    WHERE status = 'aktivni';

-- offers: ponudba kupca na oglas.
CREATE TABLE IF NOT EXISTS offers (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    listing_id BIGINT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    buyer_id   BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    amount_eur NUMERIC(10,2) NOT NULL,
    message    TEXT,
    status     offer_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    decided_at TIMESTAMPTZ,

    CONSTRAINT offer_amount_positive CHECK (amount_eur > 0)
);

CREATE INDEX IF NOT EXISTS idx_offers_listing ON offers (listing_id);
CREATE INDEX IF NOT EXISTS idx_offers_buyer   ON offers (buyer_id);
CREATE INDEX IF NOT EXISTS idx_offers_pending
    ON offers (listing_id)
    WHERE status = 'pending';

-- "Največ ena accepted ponudba na oglas" – uveljavljeno na ravni baze.
CREATE UNIQUE INDEX IF NOT EXISTS idx_offers_one_accepted_per_listing
    ON offers (listing_id)
    WHERE status = 'accepted';
