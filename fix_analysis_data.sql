-- Fix Analysis Data Retrieval
-- This script updates the database functions to include all necessary analysis fields

-- Update the get_complete_conversation_data function to include all analysis fields
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

-- Grant necessary permissions
GRANT EXECUTE ON FUNCTION get_complete_conversation_data(UUID, UUID) TO authenticated;

-- Create a function to get analysis data with all fields
CREATE OR REPLACE FUNCTION get_analysis_with_all_fields(p_conversation_id UUID, p_user_id UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
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
    ) INTO result
    FROM analysis a
    WHERE a.conversation_id = p_conversation_id AND a.user_id = p_user_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions
GRANT EXECUTE ON FUNCTION get_analysis_with_all_fields(UUID, UUID) TO authenticated;

-- Verify the functions were created successfully
SELECT 'Functions updated successfully' as status; 