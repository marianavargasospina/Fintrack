CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES accounts(id),
    category_id UUID REFERENCES categories(id),
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense', 'transfer')),
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    description VARCHAR(255),
    transaction_date DATE NOT NULL,
    destination_account_id UUID REFERENCES accounts(id),
    CHECK (
        (type = 'transfer'
            AND category_id IS NULL
            AND destination_account_id IS NOT NULL
            AND account_id <> destination_account_id)
        OR
        (type IN ('income', 'expense')
            AND category_id IS NOT NULL
            AND destination_account_id IS NULL)
    )
);

CREATE INDEX IF NOT EXISTS ix_transactions_user_date
    ON transactions (user_id, transaction_date DESC);
CREATE INDEX IF NOT EXISTS ix_transactions_account_id ON transactions (account_id);
CREATE INDEX IF NOT EXISTS ix_transactions_category_id ON transactions (category_id);

ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public' AND tablename = 'transactions'
          AND policyname = 'transactions_user_isolation'
    ) THEN
        CREATE POLICY transactions_user_isolation ON transactions
            USING (user_id = current_setting('app.current_user_id')::uuid)
            WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);
    END IF;
END
$$;