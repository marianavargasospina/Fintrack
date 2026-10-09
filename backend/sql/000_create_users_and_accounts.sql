CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('cash', 'bank', 'savings', 'credit_card')),
    currency VARCHAR(3) NOT NULL DEFAULT 'COP',
    current_balance NUMERIC(14, 2) NOT NULL DEFAULT 0,
    CHECK (currency = upper(currency)),
    UNIQUE (user_id, name)
);

CREATE INDEX IF NOT EXISTS ix_accounts_user_id ON accounts (user_id);

ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename = 'accounts'
          AND policyname = 'accounts_user_isolation'
    ) THEN
        CREATE POLICY accounts_user_isolation ON accounts
            USING (user_id = current_setting('app.current_user_id')::uuid)
            WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);
    END IF;
END
$$;
