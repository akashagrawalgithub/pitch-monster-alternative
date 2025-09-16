"""
Backend API endpoints for database operations
Separated from core app.py functionality for better organization
"""

from flask import Blueprint, request, jsonify
from database_operations import DatabaseManager
from prompt_manager import prompt_manager
from user_manager import user_manager
from datetime import datetime
import json
import uuid
import time

# Create Blueprint for database API routes
db_api = Blueprint('db_api', __name__)

# Initialize Database Manager
db = DatabaseManager()

def get_current_user_id():
    """Get current user ID from request headers using custom JWT auth"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("No valid Authorization header found")
            return None
        
        token = auth_header.split(' ')[1]
        # Removed logging for performance
        
        # Use our custom user manager to verify the token
        payload = user_manager.verify_token(token)
        
        if payload and 'user_id' in payload:
            # Removed logging for performance
            return payload['user_id']
        else:
            print("No valid user ID in token payload")
            return None
            
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None

def get_user_role():
    """Get current user role from request headers using custom JWT auth"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("No valid Authorization header found")
            return None
        
        token = auth_header.split(' ')[1]
        
        # Use our custom user manager to verify the token
        payload = user_manager.verify_token(token)
        
        if payload and 'role' in payload:
            # Removed logging for performance
            return payload['role']
        else:
            print("No valid role in token payload")
            return None
            
    except Exception as e:
        print(f"Error getting user role: {e}")
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
        
        # Get agent_id from request data
        agent_id = data.get("agent_id")
        
        # Prepare conversation data with all schema fields
        conversation_data = {
            "user_id": user_id,
            "agent_id": agent_id,
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
            # Removed logging for performance
            return jsonify({
                "success": True,
                "conversation_id": result["conversation_id"],
                "message": "Conversation saved successfully"
            })
        else:
            # Removed logging for performance
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
            # Removed logging for performance
            return jsonify({
                "success": True,
                "analysis_id": result["analysis_id"],
                "conversation_id": conversation_id,
                "message": "Analysis saved successfully"
            })
        else:
            # Removed logging for performance
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
            # Removed logging for performance
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
        start_time = time.time()
        
        # Get user from auth token
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.json
        conversation_id = data.get("conversation_id")
        
        if not conversation_id:
            return jsonify({"error": "Missing conversation_id"}), 400
        
        print(f"🔍 DEBUG: Checking best pitch for conversation_id: {conversation_id}, user_id: {user_id}")
        
        # Check if best pitch exists
        existing_best_pitch = db.get_conversation_best_pitch(conversation_id, user_id)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ Best pitch check completed in {execution_time:.2f}ms")
        
        if existing_best_pitch:
            print(f"✅ Best pitch found in database for conversation {conversation_id}")
            return jsonify({
                "success": True,
                "exists": True,
                "best_pitch_id": existing_best_pitch["id"],
                "data": {
                    "perfect_conversation": existing_best_pitch.get("perfect_conversation", []),
                    "overall_improvements": existing_best_pitch.get("overall_improvements", {}),
                    "score_improvement": existing_best_pitch.get("score_improvement", {})
                },
                "execution_time_ms": round(execution_time, 2)
            })
        else:
            print(f"❌ No best pitch found for conversation {conversation_id}")
            return jsonify({
                "success": True,
                "exists": False,
                "execution_time_ms": round(execution_time, 2)
            })
        
    except Exception as e:
        print(f"Error checking best pitch: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }), 500

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

@db_api.route('/get_all_conversations_admin', methods=['GET'])
def get_all_conversations_admin():
    """Get all conversations for admin users - includes user information"""
    try:
        start_time = time.time()
        
        # Get current user ID and check if admin
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        
        # Check if user is admin
        user_role = get_user_role()
        if user_role != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        # Get all conversations with user information using admin method
        conversations = db.get_all_conversations_admin_optimized()
        
        execution_time = (time.time() - start_time) * 1000
        print(f"✅ API: All conversations (admin) retrieved in {execution_time:.2f}ms")
        
        return jsonify({
            'success': True,
            'conversations': conversations,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        print(f"Error getting conversations (admin): {e}")
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
        
        print(f"🔍 DEBUG: Looking for conversation_id: {conversation_id}, user_id: {user_id}")
        
        # Check if user is admin - if so, bypass user_id filter
        user_role = get_user_role()
        is_admin = user_role == 'admin'
        
        if is_admin:
            print(f"🔍 DEBUG: Admin user detected, bypassing user_id filter")
            # For admin users, get conversation without user_id filter
            conversation = db.get_conversation_by_id_admin(conversation_id)
        else:
            # For regular users, get conversation with user_id filter
            conversation = db.get_conversation_by_id_optimized(conversation_id, user_id)
        
        if not conversation:
            print(f"❌ DEBUG: Conversation not found for conversation_id: {conversation_id}, user_id: {user_id}")
            # Let's check if the conversation exists at all (without user filter)
            all_conversations = db.supabase.table('conversations').select('id,user_id,title').execute()
            if all_conversations.data:
                print(f"🔍 DEBUG: Available conversations: {[c.get('id') for c in all_conversations.data]}")
                print(f"🔍 DEBUG: Conversation user IDs: {[c.get('user_id') for c in all_conversations.data]}")
            return jsonify({'success': False, 'error': 'Conversation not found'}), 404
        
        print(f"🔍 DEBUG: Conversation found: {conversation.get('id')}")
        print(f"🔍 DEBUG: Conversation keys: {list(conversation.keys())}")
        
        # For admin users, get analysis without user_id filter
        if is_admin:
            analysis = db.get_analysis_by_conversation_id_admin(conversation_id)
        else:
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

@db_api.route('/debug/conversations', methods=['GET'])
def debug_conversations():
    """Debug endpoint to check all conversations in database"""
    try:
        # Get all conversations without user filter
        response = db.supabase.table('conversations').select('*').execute()
        
        return jsonify({
            "success": True,
            "total_conversations": len(response.data) if response.data else 0,
            "conversations": response.data if response.data else []
        })
        
    except Exception as e:
        print(f"Error in debug endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@db_api.route('/my-conversations', methods=['GET'])
def get_my_conversations():
    """Get conversations for the current authenticated user"""
    try:
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get conversations for the current user
        response = db.supabase.table('conversations').select(
            'id,title,session_id,created_at,status,total_exchanges,duration_seconds'
        ).eq('user_id', user_id).order('created_at', desc=True).execute()
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "total_conversations": len(response.data) if response.data else 0,
            "conversations": response.data if response.data else []
        })
        
    except Exception as e:
        print(f"Error getting user conversations: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@db_api.route('/debug/users', methods=['GET'])
def debug_users():
    """Debug endpoint to check all users in database"""
    try:
        # Get all users
        response = db.supabase.table('users').select('id,email,first_name,last_name,role,created_at').execute()
        
        return jsonify({
            "success": True,
            "total_users": len(response.data) if response.data else 0,
            "users": response.data if response.data else []
        })
        
    except Exception as e:
        print(f"Error in debug users endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@db_api.route('/fix-user-ids', methods=['POST'])
def fix_user_ids():
    """Fix user IDs to match Supabase Auth UIDs"""
    try:
        # Update admin user ID
        db.supabase.table('users').update({
            'id': '80c86068-67ea-4e01-a4e2-d199c5ef48d5'
        }).eq('email', 'admin@example.com').execute()
        
        # Update akash242018 user ID
        db.supabase.table('users').update({
            'id': '84fdf21e-9990-4c37-aba7-014a815e15a3'
        }).eq('email', 'akash242018@gmail.com').execute()
        
        return jsonify({
            "success": True,
            "message": "User IDs updated to match Supabase Auth UIDs"
        })
        
    except Exception as e:
        print(f"Error fixing user IDs: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

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
        # Removed logging for performance
        
        return jsonify({
            'success': True,
            'agents': agents,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        # Removed logging for performance
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

# PROMPT MANAGEMENT API ENDPOINTS
@db_api.route('/get_agent_prompt', methods=['POST'])
def get_agent_prompt():
    """Get the current prompt for a specific agent"""
    try:
        data = request.get_json()
        agent_key = data.get('agent_key')
        
        if not agent_key:
            return jsonify({'success': False, 'error': 'Agent key required'}), 400
        
        # Get prompt from memory (no DB call)
        prompt = prompt_manager.get_prompt(agent_key)
        
        return jsonify({
            'success': True,
            'agent_key': agent_key,
            'prompt': prompt
        })
        
    except Exception as e:
        print(f"Error getting agent prompt: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_all_prompts', methods=['GET'])
def get_all_prompts():
    """Get all agent prompts (from memory)"""
    try:
        # Get all prompts from memory (no DB call)
        prompts = prompt_manager.get_all_prompts()
        
        return jsonify({
            'success': True,
            'prompts': prompts
        })
        
    except Exception as e:
        print(f"Error getting all prompts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/update_agent_prompt', methods=['POST'])
def update_agent_prompt():
    """Update the prompt for a specific agent"""
    try:
        data = request.get_json()
        agent_key = data.get('agent_key')
        new_prompt = data.get('prompt')
        
        if not agent_key:
            return jsonify({'success': False, 'error': 'Agent key required'}), 400
        
        if not new_prompt:
            return jsonify({'success': False, 'error': 'Prompt content required'}), 400
        
        # Update prompt in both DB and memory
        success = prompt_manager.update_prompt(agent_key, new_prompt)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Prompt updated successfully for agent: {agent_key}'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update prompt'}), 500
        
    except Exception as e:
        print(f"Error updating agent prompt: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/update_agent_sample_script', methods=['POST'])
def update_agent_sample_script():
    """Update the sample script for a specific agent"""
    try:
        data = request.get_json()
        agent_key = data.get('agent_key')
        sample_script = data.get('sample_script')
        
        if not agent_key:
            return jsonify({'success': False, 'error': 'Agent key required'}), 400
        
        if not sample_script:
            return jsonify({'success': False, 'error': 'Sample script content required'}), 400
        
        # Update sample script using prompt manager (updates both DB and memory)
        success = prompt_manager.update_sample_script(agent_key, sample_script)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Sample script updated successfully for agent: {agent_key}'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update sample script'}), 500
        
    except Exception as e:
        print(f"Error updating agent sample script: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/reload_prompts', methods=['POST'])
def reload_prompts():
    """Reload all prompts from database"""
    try:
        # Reload prompts from database
        success = prompt_manager.reload_prompts()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Prompts reloaded successfully from database'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to reload prompts'}), 500
        
    except Exception as e:
        print(f"Error reloading prompts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/get_agent_with_prompt', methods=['POST'])
def get_agent_with_prompt():
    """Get full agent information including prompt"""
    try:
        data = request.get_json()
        agent_key = data.get('agent_key')
        
        if not agent_key:
            return jsonify({'success': False, 'error': 'Agent key required'}), 400
        
        # Get agent info including prompt
        agent_info = prompt_manager.get_agent_info(agent_key)
        
        if not agent_info:
            return jsonify({'success': False, 'error': 'Agent not found'}), 404
        
        return jsonify({
            'success': True,
            'agent': agent_info
        })
        
    except Exception as e:
        print(f"Error getting agent with prompt: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# USER MANAGEMENT API ENDPOINTS
@db_api.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Authenticate user
        user_data = user_manager.authenticate_user(email, password)
        
        if user_data:
            return jsonify({
                'success': True,
                'user': user_data,
                'message': 'Login successful'
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        # Removed logging for performance
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Create user
        user_data = user_manager.create_user(email, password, first_name, last_name)
        
        if user_data:
            return jsonify({
                'success': True,
                'user': user_data,
                'message': 'User created successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'User already exists'}), 409
        
    except Exception as e:
        print(f"Error in registration: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if payload:
            user_data = user_manager.get_user_by_id(payload['user_id'])
            if user_data:
                return jsonify({
                    'success': True,
                    'user': user_data
                })
        
        return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
    except Exception as e:
        print(f"Error checking auth: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/users/get_all', methods=['GET'])
def get_all_users():
    """Get all users (admin only)"""
    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        # Get all users
        users = user_manager.get_all_users(payload['user_id'])
        
        return jsonify({
            'success': True,
            'users': users
        })
        
    except Exception as e:
        print(f"Error getting all users: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/users/update_role', methods=['POST'])
def update_user_role():
    """Update user role (admin only)"""
    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        data = request.get_json()
        target_user_id = data.get('user_id')
        new_role = data.get('role')
        
        if not target_user_id or not new_role:
            return jsonify({'success': False, 'error': 'User ID and role required'}), 400
        
        # Update user role
        success = user_manager.update_user_role(target_user_id, new_role, payload['user_id'])
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User role updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update user role'}), 403
        
    except Exception as e:
        print(f"Error updating user role: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/users/deactivate', methods=['POST'])
def deactivate_user():
    """Deactivate user (admin only)"""
    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        data = request.get_json()
        target_user_id = data.get('user_id')
        
        if not target_user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        
        # Deactivate user
        success = user_manager.deactivate_user(target_user_id, payload['user_id'])
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User deactivated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to deactivate user'}), 401
        
    except Exception as e:
        print(f"Error deactivating user: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/users/activate', methods=['POST'])
def activate_user():
    """Activate user (admin only)"""
    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        data = request.get_json()
        target_user_id = data.get('user_id')
        
        if not target_user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        
        # Activate user
        success = user_manager.activate_user(target_user_id, payload['user_id'])
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User activated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to activate user'}), 403
        
    except Exception as e:
        print(f"Error activating user: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/users/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics (admin only)"""
    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        # Get user stats
        stats = user_manager.get_user_stats(payload['user_id'])
        
        if stats:
            return jsonify({
                'success': True,
                'stats': stats
            })
        else:
            return jsonify({'success': False, 'error': 'Access denied'}), 403
        
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@db_api.route('/conversation/stats', methods=['GET'])
def get_conversation_stats():
    """Get conversation statistics (admin only)"""
    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = user_manager.verify_token(token)
        
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        # Check if user is admin
        if not user_manager.is_admin(payload['user_id']):
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        # Get conversation statistics
        stats = db.get_conversation_stats()
        
        if stats:
            return jsonify({
                'success': True,
                'stats': stats
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch statistics'}), 500
        
    except Exception as e:
        print(f"Error getting conversation stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500