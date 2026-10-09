CREATE TABLE savings_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    target_amount NUMERIC(14, 2) NOT NULL CHECK (target_amount > 0),
    current_amount NUMERIC(14, 2) NOT NULL DEFAULT 0 CHECK (current_amount >= 0),
    target_date DATE NOT NULL,
    CHECK (current_amount <= target_amount)
);

CREATE INDEX ix_savings_goals_user_id ON savings_goals (user_id);
ALTER TABLE savings_goals ENABLE ROW LEVEL SECURITY;
CREATE POLICY savings_goals_user_isolation ON savings_goals
    USING (user_id = current_setting('app.current_user_id')::uuid)
    WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);