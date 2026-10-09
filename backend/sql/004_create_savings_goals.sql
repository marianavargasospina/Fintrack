CREATE TABLE IF NOT EXISTS savings_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    target_amount NUMERIC(14, 2) NOT NULL CHECK (target_amount > 0),
    current_amount NUMERIC(14, 2) NOT NULL DEFAULT 0 CHECK (current_amount >= 0),
    target_date DATE NOT NULL,
    CHECK (current_amount <= target_amount)
);

CREATE INDEX IF NOT EXISTS ix_savings_goals_user_id ON savings_goals (user_id);
ALTER TABLE savings_goals ENABLE ROW LEVEL SECURITY;
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public' AND tablename = 'savings_goals'
          AND policyname = 'savings_goals_user_isolation'
    ) THEN
        CREATE POLICY savings_goals_user_isolation ON savings_goals
            USING (user_id = current_setting('app.current_user_id')::uuid)
            WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);
    END IF;
END
$$;