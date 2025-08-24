-- PERFORMANCE OPTIMIZATION SCRIPT
-- Apply this script to your Supabase database to improve query performance
-- Note: This script only includes optimizations that work within Supabase's constraints

-- 1. Create database indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_conversations_user_id_created_at ON conversations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_id_user_id ON conversations(id, user_id);
CREATE INDEX IF NOT EXISTS idx_analysis_conversation_id_user_id ON analysis(conversation_id, user_id);
CREATE INDEX IF NOT EXISTS idx_best_pitch_conversation_id_user_id ON best_pitch(conversation_id, user_id);

-- 2. Create optimized RPC function for getting complete conversation data
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
                'session_info', a.session_info,
                'voice_delivery_analysis', a.voice_delivery_analysis,
                'sales_skills_assessment', a.sales_skills_assessment,
                'sales_process_flow', a.sales_process_flow,
                'detailed_feedback', a.detailed_feedback,
                'recommendations', a.recommendations,
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

-- 3. Create optimized function for getting user conversations with summary
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

-- 4. Create materialized view for conversation summaries
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

-- 5. Create index on materialized view
CREATE INDEX IF NOT EXISTS idx_conversation_summary_mv_user_id ON conversation_summary_mv(user_id, conversation_created DESC);

-- 6. Function to refresh materialized view
CREATE OR REPLACE FUNCTION refresh_conversation_summary()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW conversation_summary_mv;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 7. Trigger to automatically refresh materialized view when data changes
CREATE OR REPLACE FUNCTION trigger_refresh_conversation_summary()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM refresh_conversation_summary();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 8. Create triggers for automatic refresh
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

-- 9. Grant permissions for the new functions
GRANT EXECUTE ON FUNCTION get_complete_conversation_data(UUID, UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_conversations_optimized(UUID, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION refresh_conversation_summary() TO authenticated;

-- 10. Grant permissions for materialized view
GRANT SELECT ON conversation_summary_mv TO authenticated;

-- 11. Initial refresh of materialized view
SELECT refresh_conversation_summary();

-- 12. Analyze tables for better query planning
ANALYZE conversations;
ANALYZE analysis;
ANALYZE best_pitch;
ANALYZE conversation_summary_mv;

-- 13. Set session-level optimizations (these work in Supabase)
-- Note: These settings apply to the current session only
SET work_mem = '4MB';
SET maintenance_work_mem = '64MB';
SET effective_cache_size = '1GB';
SET plan_cache_mode = 'auto';
SET random_page_cost = 1.1;
SET effective_io_concurrency = 200;
SET seq_page_cost = 1.0;
SET max_parallel_workers_per_gather = 2;
SET max_parallel_workers = 4;

-- Success message
SELECT 'Performance optimizations applied successfully!' as status; 