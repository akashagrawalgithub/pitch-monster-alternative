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