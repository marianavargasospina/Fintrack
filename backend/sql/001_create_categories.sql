CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    UNIQUE (user_id, name, type)
);

CREATE INDEX IF NOT EXISTS ix_categories_user_id ON categories (user_id);

ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public' AND tablename = 'categories'
          AND policyname = 'categories_user_isolation'
    ) THEN
        CREATE POLICY categories_user_isolation ON categories
            USING (user_id = current_setting('app.current_user_id')::uuid)
            WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);
    END IF;
END
$$;