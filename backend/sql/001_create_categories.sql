CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    UNIQUE (user_id, name, type)
);

CREATE INDEX ix_categories_user_id ON categories (user_id);

ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY categories_user_isolation ON categories
    USING (user_id = current_setting('app.current_user_id')::uuid)
    WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);