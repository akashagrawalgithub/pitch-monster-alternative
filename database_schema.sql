-- Database Schema for Voice Web Chat Application
-- Supabase SQL queries to create the required tables

-- 1. CONVERSATIONS TABLE
-- Stores conversation data including audio, transcript, and user information
CREATE TABLE conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    session_id UUID DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Conversation metadata
    title VARCHAR(255),
    duration_seconds INTEGER,
    total_exchanges INTEGER DEFAULT 0,
    
    -- Full conversation data
    full_conversation JSONB NOT NULL, -- Array of {user: string, assistant: string, timestamp: string}
    transcript JSONB, -- Array of {sender: string, text: string, time: string}
    
    -- Audio data (base64 encoded)
    audio_data TEXT, -- Base64 encoded audio file
    audio_format VARCHAR(50) DEFAULT 'pcm_f32le',
    sample_rate INTEGER DEFAULT 44100,
    audio_duration_seconds DECIMAL(10,2),
    
    -- User session info
    user_agent TEXT,
    ip_address INET,
    
    -- Status and metadata
    status VARCHAR(50) DEFAULT 'active',
    tags TEXT[],
    notes TEXT
);

-- 2. ANALYSIS TABLE
-- Stores analysis results linked to conversations
CREATE TABLE analysis (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Analysis metadata
    analysis_version VARCHAR(20) DEFAULT '1.0',
    model_used VARCHAR(100) DEFAULT 'gpt-4o-mini',
    
    -- Session information
    session_info JSONB, -- {session_duration, total_exchanges, etc.}
    
    -- Overall scoring
    overall_score JSONB, -- {percentage: number, grade: string, breakdown: object}
    
    -- Key metrics
    key_metrics JSONB, -- {clarity_score, engagement_score, etc.}
    
    -- Voice delivery analysis
    voice_delivery_analysis JSONB, -- {tone, pace, clarity, etc. with 0-100 scores}
    
    -- Sales skills assessment
    sales_skills_assessment JSONB, -- {questioning, objection_handling, etc. with 1-5 star ratings}
    
    -- Sales process flow
    sales_process_flow JSONB, -- {stages: array of {stage: string, status: string, score: number}}
    
    -- Strengths and improvements
    strengths JSONB, -- Array of strength descriptions
    improvements JSONB, -- Array of improvement suggestions
    
    -- Additional analysis data
    detailed_feedback JSONB,
    recommendations JSONB,
    
    -- Status
    status VARCHAR(50) DEFAULT 'completed'
);

-- 3. BEST_PITCH TABLE
-- Stores perfect pitch versions and improvements
CREATE TABLE best_pitch (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    analysis_id UUID REFERENCES analysis(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Perfect conversation data
    perfect_conversation JSONB NOT NULL, -- Array of improved exchanges
    original_conversation JSONB, -- Reference to original conversation
    
    -- Score improvements
    score_improvement JSONB, -- {original_score: number, perfect_score: number, improvement: number}
    overall_improvements JSONB, -- Detailed improvement breakdown
    
    -- Model information
    model_used VARCHAR(100) DEFAULT 'gpt-4o-mini',
    generation_version VARCHAR(20) DEFAULT '1.0',
    
    -- Additional data
    key_changes JSONB, -- Array of specific changes made
    improvement_areas JSONB, -- Areas that were improved
    best_practices_applied JSONB, -- Sales best practices used
    
    -- Status
    status VARCHAR(50) DEFAULT 'completed'
);

-- Create indexes for better performance
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);

CREATE INDEX idx_analysis_conversation_id ON analysis(conversation_id);
CREATE INDEX idx_analysis_user_id ON analysis(user_id);
CREATE INDEX idx_analysis_created_at ON analysis(created_at);

CREATE INDEX idx_best_pitch_conversation_id ON best_pitch(conversation_id);
CREATE INDEX idx_best_pitch_analysis_id ON best_pitch(analysis_id);
CREATE INDEX idx_best_pitch_user_id ON best_pitch(user_id);
CREATE INDEX idx_best_pitch_created_at ON best_pitch(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to conversations table
CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON conversations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE best_pitch ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for conversations
CREATE POLICY "Users can view their own conversations" ON conversations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own conversations" ON conversations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own conversations" ON conversations
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own conversations" ON conversations
    FOR DELETE USING (auth.uid() = user_id);

-- Create RLS policies for analysis
CREATE POLICY "Users can view their own analysis" ON analysis
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own analysis" ON analysis
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own analysis" ON analysis
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own analysis" ON analysis
    FOR DELETE USING (auth.uid() = user_id);

-- Create RLS policies for best_pitch
CREATE POLICY "Users can view their own best pitch" ON best_pitch
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own best pitch" ON best_pitch
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own best pitch" ON best_pitch
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own best pitch" ON best_pitch
    FOR DELETE USING (auth.uid() = user_id);

-- Create a view for easy querying of conversation with analysis and best pitch
CREATE VIEW conversation_summary AS
SELECT 
    c.id as conversation_id,
    c.user_id,
    c.session_id,
    c.created_at as conversation_created,
    c.title,
    c.duration_seconds,
    c.total_exchanges,
    c.status as conversation_status,
    
    -- Analysis data
    a.id as analysis_id,
    a.created_at as analysis_created,
    a.overall_score,
    a.key_metrics,
    a.status as analysis_status,
    
    -- Best pitch data
    bp.id as best_pitch_id,
    bp.created_at as best_pitch_created,
    bp.score_improvement,
    bp.status as best_pitch_status
    
FROM conversations c
LEFT JOIN analysis a ON c.id = a.conversation_id
LEFT JOIN best_pitch bp ON c.id = bp.conversation_id
ORDER BY c.created_at DESC;

-- Grant necessary permissions
GRANT ALL ON conversations TO authenticated;
GRANT ALL ON analysis TO authenticated;
GRANT ALL ON best_pitch TO authenticated;
GRANT SELECT ON conversation_summary TO authenticated; 

-- PERFORMANCE OPTIMIZATION: Add database indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_conversations_user_id_created_at ON conversations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_id_user_id ON conversations(id, user_id);
CREATE INDEX IF NOT EXISTS idx_analysis_conversation_id_user_id ON analysis(conversation_id, user_id);
CREATE INDEX IF NOT EXISTS idx_best_pitch_conversation_id_user_id ON best_pitch(conversation_id, user_id);

-- PERFORMANCE OPTIMIZATION: Create optimized RPC function for getting complete conversation data
CREATE OR REPLACE FUNCTION get_complete_conversation_data(p_conversation_id UUID, p_user_id UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'conversation', json_build_object(
            'id', c.id,
            'title', c.title,
            'session_id', c.session_id,
            'duration_seconds', c.duration_seconds,
            'total_exchanges', c.total_exchanges,
            'created_at', c.created_at,
            'updated_at', c.updated_at,
            'status', c.status
        ),
        'analysis', CASE 
            WHEN a.id IS NOT NULL THEN json_build_object(
                'id', a.id,
                'conversation_id', a.conversation_id,
                'overall_score', a.overall_score,
                'key_metrics', a.key_metrics,
                'strengths', a.strengths,
                'improvements', a.improvements,
                'created_at', a.created_at
            )
            ELSE NULL
        END,
        'best_pitch', CASE 
            WHEN bp.id IS NOT NULL THEN json_build_object(
                'id', bp.id,
                'conversation_id', bp.conversation_id,
                'analysis_id', bp.analysis_id,
                'perfect_conversation', bp.perfect_conversation,
                'score_improvement', bp.score_improvement,
                'created_at', bp.created_at
            )
            ELSE NULL
        END
    ) INTO result
    FROM conversations c
    LEFT JOIN analysis a ON c.id = a.conversation_id AND a.user_id = p_user_id
    LEFT JOIN best_pitch bp ON c.id = bp.conversation_id AND bp.user_id = p_user_id
    WHERE c.id = p_conversation_id AND c.user_id = p_user_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- PERFORMANCE OPTIMIZATION: Create optimized function for getting user conversations with summary
CREATE OR REPLACE FUNCTION get_user_conversations_optimized(p_user_id UUID, p_limit INTEGER DEFAULT 50)
RETURNS TABLE (
    id UUID,
    title TEXT,
    session_id TEXT,
    duration_seconds INTEGER,
    total_exchanges INTEGER,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    status TEXT,
    has_analysis BOOLEAN,
    has_best_pitch BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.title,
        c.session_id,
        c.duration_seconds,
        c.total_exchanges,
        c.created_at,
        c.updated_at,
        c.status,
        (a.id IS NOT NULL) as has_analysis,
        (bp.id IS NOT NULL) as has_best_pitch
    FROM conversations c
    LEFT JOIN analysis a ON c.id = a.conversation_id AND a.user_id = p_user_id
    LEFT JOIN best_pitch bp ON c.id = bp.conversation_id AND bp.user_id = p_user_id
    WHERE c.user_id = p_user_id
    ORDER BY c.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- PERFORMANCE OPTIMIZATION: Create materialized view for conversation summaries
CREATE MATERIALIZED VIEW IF NOT EXISTS conversation_summary_mv AS
SELECT 
    c.id as conversation_id,
    c.title as conversation_title,
    c.created_at as conversation_created,
    c.duration_seconds,
    c.total_exchanges,
    c.status,
    a.overall_score->>'percentage' as analysis_score,
    (bp.id IS NOT NULL) as best_pitch_exists,
    c.user_id
FROM conversations c
LEFT JOIN analysis a ON c.id = a.conversation_id
LEFT JOIN best_pitch bp ON c.id = bp.conversation_id
ORDER BY c.created_at DESC;

-- Create index on materialized view
CREATE INDEX IF NOT EXISTS idx_conversation_summary_mv_user_id ON conversation_summary_mv(user_id, conversation_created DESC);

-- Function to refresh materialized view
CREATE OR REPLACE FUNCTION refresh_conversation_summary()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW conversation_summary_mv;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically refresh materialized view when data changes
CREATE OR REPLACE FUNCTION trigger_refresh_conversation_summary()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM refresh_conversation_summary();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for automatic refresh
DROP TRIGGER IF EXISTS trigger_conversations_refresh_summary ON conversations;
CREATE TRIGGER trigger_conversations_refresh_summary
    AFTER INSERT OR UPDATE OR DELETE ON conversations
    FOR EACH STATEMENT
    EXECUTE FUNCTION trigger_refresh_conversation_summary();

DROP TRIGGER IF EXISTS trigger_analysis_refresh_summary ON analysis;
CREATE TRIGGER trigger_analysis_refresh_summary
    AFTER INSERT OR UPDATE OR DELETE ON analysis
    FOR EACH STATEMENT
    EXECUTE FUNCTION trigger_refresh_conversation_summary();

DROP TRIGGER IF EXISTS trigger_best_pitch_refresh_summary ON best_pitch;
CREATE TRIGGER trigger_best_pitch_refresh_summary
    AFTER INSERT OR UPDATE OR DELETE ON best_pitch
    FOR EACH STATEMENT
    EXECUTE FUNCTION trigger_refresh_conversation_summary();

-- PERFORMANCE OPTIMIZATION: Application-level optimizations
-- Note: System-level PostgreSQL parameters are managed by Supabase
-- and cannot be modified through regular SQL commands

-- Set session-level optimizations (these work in Supabase)
SET work_mem = '4MB';
SET maintenance_work_mem = '64MB';
SET effective_cache_size = '1GB';

-- Enable query plan caching for this session
SET plan_cache_mode = 'auto';

-- Optimize query planner settings
SET random_page_cost = 1.1;
SET effective_io_concurrency = 200;
SET seq_page_cost = 1.0;

-- Enable parallel query execution for this session
SET max_parallel_workers_per_gather = 2;
SET max_parallel_workers = 4; 