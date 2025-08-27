"""
Backend API endpoints for database operations
Separated from core app.py functionality for better organization
"""

from flask import Blueprint, request, jsonify
from database_operations import DatabaseManager
from datetime import datetime
import json
import uuid
import time

# Create Blueprint for database API routes
db_api = Blueprint('db_api', __name__)

# Initialize Database Manager
db = DatabaseManager()

def get_current_user_id():
    """Get current user ID from request headers using Supabase auth"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("No valid Authorization header found")
            return None
        
        token = auth_header.split(' ')[1]
        print(f"Token received: {token[:20]}...")
        
        # Set the auth token for database operations
        db.set_auth_token(token)
        
        # Use the authenticated client to get user info
        try:
            user = db.user_supabase.auth.get_user(token) if db.user_supabase else db.supabase.auth.get_user(token)
            if user and user.user:
                print(f"User ID: {user.user.id}")
                return user.user.id
            else:
                print("No user found in response")
                return None
        except Exception as auth_error:
            print(f"Token validation failed: {auth_error}")
            # Token is expired or invalid
            return None
            
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None

@db_api.route('/save_conversation', methods=['POST'])
def save_conversation():
    """Save complete conversation data when user ends the call"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Prepare conversation data with all schema fields
        conversation_data = {
            "user_id": user_id,
            "session_id": data.get("session_id") or str(uuid.uuid4()),
            "title": data.get("title", f"Sales Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
            "duration_seconds": data.get("duration_seconds", 0),
            "total_exchanges": len(data.get("conversation_history", [])),
            "full_conversation": data.get("conversation_history", []),
            "transcript": data.get("transcript", []),
            "audio_data": data.get("audio_data"),  # Base64 encoded
            "audio_format": data.get("audio_format", "pcm_f32le"),
            "sample_rate": data.get("sample_rate", 44100),
            "audio_duration_seconds": data.get("audio_duration", 0),
            "user_agent": request.headers.get("User-Agent"),
            "ip_address": request.remote_addr,
            "status": data.get("status", "completed"),
            "tags": data.get("tags", []),
            "notes": data.get("notes")
        }
        
        # Save to database
        result = db.save_conversation(user_id, conversation_data)
        
        if result["success"]:
            print(f"✅ Conversation saved successfully: {result['conversation_id']}")
            return jsonify({
                "success": True,
                "conversation_id": result["conversation_id"],
                "message": "Conversation saved successfully"
            })
        else:
            print(f"❌ Failed to save conversation: {result.get('error')}")
            return jsonify({
                "success": False,
                "error": result.get("error", "Failed to save conversation")
            }), 500
        
    except Exception as e:
        print(f"Error saving conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/save_analysis', methods=['POST'])
def save_analysis():
    """Save analysis data after analysis is complete, before redirecting to analysis screen"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        conversation_id = data.get("conversation_id")
        analysis_data = data.get("analysis_data")
        
        if not conversation_id or not analysis_data:
            return jsonify({"error": "Missing conversation_id or analysis_data"}), 400
        
        # Prepare analysis data with all schema fields
        analysis_record = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "analysis_version": data.get("analysis_version", "1.0"),
            "model_used": data.get("model_used", "gpt-4o-mini"),
            "session_info": analysis_data.get("session_info", {}),
            "overall_score": analysis_data.get("overall_score", {}),
            "key_metrics": analysis_data.get("key_metrics", {}),
            "voice_delivery_analysis": analysis_data.get("voice_delivery_analysis", {}),
            "sales_skills_assessment": analysis_data.get("sales_skills_assessment", {}),
            "sales_process_flow": analysis_data.get("sales_process_flow", {}),
            "strengths": analysis_data.get("strengths", []),
            "improvements": analysis_data.get("improvements", []),
            "detailed_feedback": analysis_data.get("detailed_feedback", {}),
            "recommendations": analysis_data.get("recommendations", {}),
            "status": data.get("status", "completed")
        }
        
        # Save analysis to database
        result = db.save_analysis(user_id, conversation_id, analysis_record)
        
        if result["success"]:
            print(f"✅ Analysis saved successfully: {result['analysis_id']}")
            return jsonify({
                "success": True,
                "analysis_id": result["analysis_id"],
                "conversation_id": conversation_id,
                "message": "Analysis saved successfully"
            })
        else:
            print(f"❌ Failed to save analysis: {result.get('error')}")
            return jsonify({
                "success": False,
                "error": result.get("error", "Failed to save analysis")
            }), 500
        
    except Exception as e:
        print(f"Error saving analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/save_best_pitch', methods=['POST'])
def save_best_pitch():
    """Save best pitch data after getting response, before showing to user"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        conversation_id = data.get("conversation_id")
        analysis_id = data.get("analysis_id")
        best_pitch_data = data.get("best_pitch_data")
        
        if not all([conversation_id, analysis_id, best_pitch_data]):
            return jsonify({"error": "Missing required fields: conversation_id, analysis_id, or best_pitch_data"}), 400
        
        # Prepare best pitch data with all schema fields
        best_pitch_record = {
            "conversation_id": conversation_id,
            "analysis_id": analysis_id,
            "user_id": user_id,
            "perfect_conversation": best_pitch_data.get("perfect_conversation", []),
            "original_conversation": data.get("original_conversation", []),
            "score_improvement": best_pitch_data.get("score_improvement", {}),
            "overall_improvements": best_pitch_data.get("overall_improvements", {}),
            "model_used": data.get("model_used", "gpt-4o-mini"),
            "generation_version": data.get("generation_version", "1.0"),
            "key_changes": best_pitch_data.get("key_changes", []),
            "improvement_areas": best_pitch_data.get("improvement_areas", []),
            "best_practices_applied": best_pitch_data.get("best_practices_applied", []),
            "status": data.get("status", "completed")
        }
        
        # Save best pitch to database
        result = db.save_best_pitch(user_id, conversation_id, analysis_id, best_pitch_record)
        
        if result["success"]:
            print(f"✅ Best pitch saved successfully: {result['best_pitch_id']}")
            return jsonify({
                "success": True,
                "best_pitch_id": result["best_pitch_id"],
                "conversation_id": conversation_id,
                "analysis_id": analysis_id,
                "message": "Best pitch saved successfully"
            })
        else:
            print(f"❌ Failed to save best pitch: {result.get('error')}")
            return jsonify({
                "success": False,
                "error": result.get("error", "Failed to save best pitch")
            }), 500
        
    except Exception as e:
        print(f"Error saving best pitch: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/conversations', methods=['GET'])
def get_user_conversations():
    """Get all conversations for the current user"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get conversations from database
        conversations = db.get_user_conversations(user_id)
        
        print(f"✅ Retrieved {len(conversations)} conversations for user {user_id}")
        return jsonify({
            "success": True,
            "conversations": conversations,
            "count": len(conversations)
        })
        
    except Exception as e:
        print(f"Error getting conversations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation_details(conversation_id):
    """Get complete conversation data including analysis and best pitch - OPTIMIZED"""
    try:
        start_time = time.time()
        
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get complete conversation data using optimized method
        data = db.get_complete_conversation_data_optimized(conversation_id, user_id)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: Complete conversation data retrieved in {execution_time:.2f}ms")
        
        if data:
            return jsonify({
                "success": True,
                "data": data,
                "execution_time_ms": round(execution_time, 2)
            })
        else:
            return jsonify({
                "success": False,
                "error": "Conversation not found"
            }), 404
        
    except Exception as e:
        print(f"Error getting conversation details: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/check_best_pitch_exists', methods=['POST'])
def check_best_pitch_exists():
    """Check if best pitch already exists for a conversation"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.json
        conversation_id = data.get("conversation_id")
        
        if not conversation_id:
            return jsonify({"error": "Missing conversation_id"}), 400
        
        # Check if best pitch exists
        existing_best_pitch = db.get_conversation_best_pitch(conversation_id, user_id)
        
        if existing_best_pitch:
            print(f"✅ Best pitch found in database for conversation {conversation_id}")
            return jsonify({
                "success": True,
                "exists": True,
                "best_pitch_id": existing_best_pitch["id"],
                "data": {
                    "perfect_conversation": existing_best_pitch["perfect_conversation"],
                    "overall_improvements": existing_best_pitch["overall_improvements"],
                    "score_improvement": existing_best_pitch["score_improvement"]
                }
            })
        else:
            print(f"❌ No best pitch found for conversation {conversation_id}")
            return jsonify({
                "success": True,
                "exists": False
            })
        
    except Exception as e:
        print(f"Error checking best pitch: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/delete_conversation/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation and all related data"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Delete conversation (will cascade to analysis and best_pitch)
        result = db.delete_conversation(conversation_id, user_id)
        
        if result:
            print(f"✅ Conversation deleted successfully: {conversation_id}")
            return jsonify({
                "success": True,
                "message": "Conversation deleted successfully"
            })
        else:
            print(f"❌ Failed to delete conversation: {conversation_id}")
            return jsonify({
                "success": False,
                "error": "Failed to delete conversation"
            }), 500
        
    except Exception as e:
        print(f"Error deleting conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/conversation_summary', methods=['GET'])
def get_conversation_summary():
    """Get conversation summary with analysis and best pitch data"""
    try:
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get limit from query params
        limit = request.args.get('limit', 20, type=int)
        
        # Get conversation summary
        summary = db.get_conversation_summary(user_id, limit)
        
        print(f"✅ Retrieved conversation summary for user {user_id}")
        return jsonify({
            "success": True,
            "summary": summary,
            "count": len(summary)
        })
        
    except Exception as e:
        print(f"Error getting conversation summary: {str(e)}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/get_all_conversations', methods=['GET'])
def get_all_conversations():
    """Get all conversations for the current user - OPTIMIZED"""
    try:
        start_time = time.time()
        
        # Get current user ID
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        
        # Get all conversations for this user using optimized method
        conversations = db.get_all_conversations_optimized(user_id)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: All conversations retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'conversations': conversations,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting conversations: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_conversation_analysis', methods=['POST'])
def get_conversation_analysis():
    """Get conversation and its analysis data - OPTIMIZED"""
    try:
        start_time = time.time()
        
        # Get current user ID
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        
        if not conversation_id:
            return jsonify({'success': False, 'error': 'Conversation ID required'}), 400
        
        # Get conversation and analysis data using optimized methods
        conversation = db.get_conversation_by_id_optimized(conversation_id, user_id)
        if not conversation:
            return jsonify({'success': False, 'error': 'Conversation not found'}), 404
        
        print(f"🔍 DEBUG: Conversation found: {conversation.get('id')}")
        print(f"🔍 DEBUG: Conversation keys: {list(conversation.keys())}")
        
        analysis = db.get_analysis_by_conversation_id_optimized(conversation_id, user_id)
        
        print(f"🔍 DEBUG: Analysis found: {analysis is not None}")
        if analysis:
            print(f"🔍 DEBUG: Analysis keys: {list(analysis.keys())}")
            print(f"🔍 DEBUG: Analysis ID: {analysis.get('id')}")
            print(f"🔍 DEBUG: Analysis conversation_id: {analysis.get('conversation_id')}")
        else:
            print(f"🔍 DEBUG: No analysis found for conversation_id: {conversation_id}")
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: Conversation analysis retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'conversation': conversation,
            'analysis': analysis,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting conversation analysis: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_client_ip', methods=['GET'])
def get_client_ip():
    """Get the client's IP address"""
    try:
        # Get IP from various headers (for proxy/load balancer scenarios)
        ip_address = request.headers.get('X-Forwarded-For', 
                       request.headers.get('X-Real-IP', 
                       request.remote_addr))
        
        # If X-Forwarded-For contains multiple IPs, take the first one
        if ip_address and ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        return jsonify({
            "success": True,
            "ip_address": ip_address or "unknown"
        })
        
    except Exception as e:
        print(f"Error getting client IP: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "ip_address": "unknown"
        }), 500

# AGENT API ENDPOINTS
@db_api.route('/get_all_agents', methods=['GET'])
def get_all_agents():
    """Get all active agents from the database"""
    try:
        start_time = time.time()
        
        # Get all agents using database method
        agents = db.get_all_agents()
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: {len(agents)} agents retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'agents': agents,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting agents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_agent_by_key', methods=['POST'])
def get_agent_by_key():
    """Get a specific agent by its key"""
    try:
        start_time = time.time()
        
        data = request.get_json()
        agent_key = data.get('agent_key')
        
        if not agent_key:
            return jsonify({'success': False, 'error': 'Agent key required'}), 400
        
        # Get agent by key using database method
        agent = db.get_agent_by_key(agent_key)
        
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not found'}), 404
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: Agent {agent_key} retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'agent': agent,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting agent by key: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_agents_by_type', methods=['POST'])
def get_agents_by_type():
    """Get all agents of a specific type"""
    try:
        start_time = time.time()
        
        data = request.get_json()
        agent_type = data.get('agent_type')
        
        if not agent_type:
            return jsonify({'success': False, 'error': 'Agent type required'}), 400
        
        # Get agents by type using database method
        agents = db.get_agents_by_type(agent_type)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: {len(agents)} agents of type {agent_type} retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'agents': agents,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting agents by type: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_agents_by_difficulty', methods=['POST'])
def get_agents_by_difficulty():
    """Get all agents of a specific difficulty level"""
    try:
        start_time = time.time()
        
        data = request.get_json()
        difficulty = data.get('difficulty')
        
        if not difficulty:
            return jsonify({'success': False, 'error': 'Difficulty level required'}), 400
        
        # Get agents by difficulty using database method
        agents = db.get_agents_by_difficulty(difficulty)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: {len(agents)} agents of difficulty {difficulty} retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'agents': agents,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting agents by difficulty: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500