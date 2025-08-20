-- Temporary fix for RLS issue - disable RLS for testing
-- Run this in your Supabase SQL editor

-- Disable RLS temporarily
ALTER TABLE conversations DISABLE ROW LEVEL SECURITY;
ALTER TABLE analysis DISABLE ROW LEVEL SECURITY;
ALTER TABLE best_pitch DISABLE ROW LEVEL SECURITY;

-- Or alternatively, create more permissive policies
DROP POLICY IF EXISTS "Users can insert their own conversations" ON conversations;
CREATE POLICY "Allow all inserts" ON conversations
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Users can insert their own analysis" ON analysis;
CREATE POLICY "Allow all analysis inserts" ON analysis
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Users can insert their own best pitch" ON best_pitch;
CREATE POLICY "Allow all best pitch inserts" ON best_pitch
    FOR INSERT WITH CHECK (true);

-- Keep the select policies for security
DROP POLICY IF EXISTS "Users can view their own conversations" ON conversations;
CREATE POLICY "Users can view their own conversations" ON conversations
    FOR SELECT USING (auth.uid() = user_id OR auth.uid() IS NULL);

DROP POLICY IF EXISTS "Users can view their own analysis" ON analysis;
CREATE POLICY "Users can view their own analysis" ON analysis
    FOR SELECT USING (auth.uid() = user_id OR auth.uid() IS NULL);

DROP POLICY IF EXISTS "Users can view their own best pitch" ON best_pitch;
CREATE POLICY "Users can view their own best pitch" ON best_pitch
    FOR SELECT USING (auth.uid() = user_id OR auth.uid() IS NULL); 