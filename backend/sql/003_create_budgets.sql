CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES categories(id),
    amount_limit NUMERIC(14, 2) NOT NULL CHECK (amount_limit > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CHECK (start_date = date_trunc('month', start_date)::date),
    CHECK (
        end_date = (
            date_trunc('month', start_date) + INTERVAL '1 month - 1 day'
        )::date
    ),
    UNIQUE (user_id, category_id, start_date)
);

CREATE INDEX ix_budgets_user_id ON budgets (user_id);
CREATE INDEX ix_budgets_category_period
    ON budgets (category_id, start_date, end_date);

ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;

CREATE POLICY budgets_user_isolation ON budgets
    USING (user_id = current_setting('app.current_user_id')::uuid)
    WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);