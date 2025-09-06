"""
Database operations for Voice Web Chat Application
Handles CRUD operations for conversations, analysis, and best_pitch tables
Optimized for performance with connection pooling and efficient queries
"""

from supabase import create_client, Client
from datetime import datetime
import json
import base64
from typing import Dict, List, Optional, Any
import uuid
import os
import time
from functools import lru_cache


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

class DatabaseManager:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self.current_token = None
        self.user_supabase = None
        # Enable connection pooling and optimize settings
        self._setup_optimizations()
    
    def _setup_optimizations(self):
        """Setup database optimizations for better performance"""
        # Configure connection pooling and other optimizations
        # Note: Supabase client handles connection pooling automatically
        pass
    
    def set_auth_token(self, access_token: str):
        """Set the authentication token for database operations"""
        self.current_token = access_token
        # Create a new client with the user's access token
        if access_token:
            try:
                self.user_supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
                # Set the auth token for this client
                self.user_supabase.auth.set_session(access_token, None)
            except Exception as e:
                print(f"Error setting auth token: {e}")
                # Fallback to anon client
                self.user_supabase = self.supabase
    
    def _get_client(self):
        """Get the appropriate Supabase client - Updated for custom JWT auth"""
        # Since we're using custom JWT authentication, always use the service role client
        return self.supabase
    
    def _refresh_token_if_needed(self):
        """Refresh the token if it's expired - Updated for custom JWT auth"""
        # Since we're using custom JWT authentication, we don't need to refresh Supabase tokens
        # The token validation is handled by the user_manager in the API endpoints
        return True
    
    def get_current_user_id(self, access_token: str) -> Optional[str]:
        """Get current user ID from access token"""
        try:
            user = self.supabase.auth.get_user(access_token)
            return user.id if user else None
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
    
    # OPTIMIZED CONVERSATION OPERATIONS
    def save_conversation(self, user_id: str, conversation_data: Dict) -> Dict:
        """Save a new conversation to the database with complete schema data"""
        try:
            start_time = time.time()
            
            # Get the appropriate client
            client = self._get_client()
            
            # Use the complete conversation data as provided
            conversation_record = conversation_data.copy()
            conversation_record["user_id"] = user_id
            
            # Ensure required fields are present
            if "session_id" not in conversation_record:
                conversation_record["session_id"] = str(uuid.uuid4())
            if "created_at" not in conversation_record:
                conversation_record["created_at"] = datetime.now().isoformat()
            if "updated_at" not in conversation_record:
                conversation_record["updated_at"] = datetime.now().isoformat()
            
            # Insert into database
            result = client.table("conversations").insert(conversation_record).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation saved in {execution_time:.2f}ms")
            
            if result.data:
                return {
                    "success": True,
                    "conversation_id": result.data[0]["id"],
                    "session_id": result.data[0]["session_id"]
                }
            else:
                return {"success": False, "error": "Failed to save conversation"}
                
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return {"success": False, "error": str(e)}
    
    def get_conversation(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID - Optimized with specific columns"""
        try:
            start_time = time.time()
            
            # Select only necessary columns for better performance
            result = self.supabase.table("conversations").select(
                "id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status"
            ).eq("id", conversation_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation retrieved in {execution_time:.2f}ms")
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None
    
    def get_user_conversations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get all conversations for a user - Optimized with specific columns"""
        try:
            start_time = time.time()
            
            # Select only necessary columns and add index hints
            result = self.supabase.table("conversations").select(
                "id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status"
            ).eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ {len(result.data)} conversations retrieved in {execution_time:.2f}ms")
            
            return result.data
        except Exception as e:
            print(f"Error getting user conversations: {e}")
            return []
    
    def update_conversation(self, conversation_id: str, user_id: str, updates: Dict) -> bool:
        """Update a conversation"""
        try:
            start_time = time.time()
            
            result = self.supabase.table("conversations").update(updates).eq("id", conversation_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation updated in {execution_time:.2f}ms")
            
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating conversation: {e}")
            return False
    
    def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Delete a conversation (will cascade to analysis and best_pitch)"""
        try:
            start_time = time.time()
            
            result = self.supabase.table("conversations").delete().eq("id", conversation_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation deleted in {execution_time:.2f}ms")
            
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    # OPTIMIZED ANALYSIS OPERATIONS
    def save_analysis(self, user_id: str, conversation_id: str, analysis_data: Dict) -> Dict:
        """Save analysis results to the database with complete schema data"""
        try:
            start_time = time.time()
            
            # Use the complete analysis data as provided
            analysis_record = analysis_data.copy()
            analysis_record["conversation_id"] = conversation_id
            analysis_record["user_id"] = user_id
            
            # Ensure required fields are present
            if "created_at" not in analysis_record:
                analysis_record["created_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("analysis").insert(analysis_record).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Analysis saved in {execution_time:.2f}ms")
            
            if result.data:
                return {
                    "success": True,
                    "analysis_id": result.data[0]["id"]
                }
            else:
                return {"success": False, "error": "Failed to save analysis"}
                
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return {"success": False, "error": str(e)}
    
    def get_analysis(self, analysis_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific analysis by ID - Optimized"""
        try:
            start_time = time.time()
            
            result = self.supabase.table("analysis").select(
                "id,conversation_id,overall_score,key_metrics,strengths,improvements,created_at"
            ).eq("id", analysis_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Analysis retrieved in {execution_time:.2f}ms")
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting analysis: {e}")
            return None
    
    def get_conversation_analysis(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get analysis for a specific conversation - Optimized"""
        try:
            start_time = time.time()
            
            result = self.supabase.table("analysis").select(
                "id,conversation_id,overall_score,key_metrics,strengths,improvements,created_at"
            ).eq("conversation_id", conversation_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation analysis retrieved in {execution_time:.2f}ms")
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting conversation analysis: {e}")
            return None
    
    # OPTIMIZED BEST PITCH OPERATIONS
    def save_best_pitch(self, user_id: str, conversation_id: str, analysis_id: str, best_pitch_data: Dict) -> Dict:
        """Save best pitch results to the database with complete schema data"""
        try:
            start_time = time.time()
            
            # Get the appropriate client
            client = self._get_client()
            
            # Use the complete best pitch data as provided
            best_pitch_record = best_pitch_data.copy()
            best_pitch_record["conversation_id"] = conversation_id
            best_pitch_record["analysis_id"] = analysis_id
            best_pitch_record["user_id"] = user_id
            
            # Ensure required fields are present
            if "created_at" not in best_pitch_record:
                best_pitch_record["created_at"] = datetime.now().isoformat()
            
            print(f"🔍 DEBUG: Saving best pitch for conversation_id: {conversation_id}, analysis_id: {analysis_id}")
            print(f"🔍 DEBUG: Best pitch record keys: {list(best_pitch_record.keys())}")
            print(f"🔍 DEBUG: User ID: {user_id}")
            
            result = client.table("best_pitch").insert(best_pitch_record).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Best pitch saved in {execution_time:.2f}ms")
            
            if result.data:
                return {
                    "success": True,
                    "best_pitch_id": result.data[0]["id"]
                }
            else:
                return {"success": False, "error": "Failed to save best pitch"}
                
        except Exception as e:
            print(f"Error saving best pitch: {e}")
            return {"success": False, "error": str(e)}
    
    def get_best_pitch(self, best_pitch_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific best pitch by ID - Optimized"""
        try:
            start_time = time.time()
            
            # Get the appropriate client
            client = self._get_client()
            
            result = client.table("best_pitch").select(
                "id,conversation_id,analysis_id,perfect_conversation,score_improvement,created_at"
            ).eq("id", best_pitch_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Best pitch retrieved in {execution_time:.2f}ms")
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting best pitch: {e}")
            return None
    
    def get_conversation_best_pitch(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get best pitch for a specific conversation - Optimized"""
        try:
            start_time = time.time()
            
            # Use service role client to bypass RLS restrictions since we're using custom JWT auth
            # The auth.uid() function in RLS policies doesn't work with custom JWT tokens
            client = self.supabase  # This is the service role client
            
            print(f"🔍 DEBUG: Fetching best pitch for conversation_id: {conversation_id}")
            print(f"🔍 DEBUG: Using service role client to bypass RLS")
            
            # First, let's check what's in the best_pitch table for this conversation
            all_best_pitches = client.table("best_pitch").select("*").eq("conversation_id", conversation_id).execute()
            print(f"🔍 DEBUG: All best pitches for conversation {conversation_id}: {all_best_pitches.data}")
            
            # Only filter by conversation_id, not by user_id, since best pitch is conversation-specific
            result = client.table("best_pitch").select(
                "id,conversation_id,analysis_id,perfect_conversation,score_improvement,created_at,overall_improvements"
            ).eq("conversation_id", conversation_id).execute()
            
            print(f"🔍 DEBUG: Best pitch response data: {result.data}")
            print(f"🔍 DEBUG: Best pitch response count: {len(result.data) if result.data else 0}")
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation best pitch retrieved in {execution_time:.2f}ms")
            
            if result.data:
                best_pitch_data = result.data[0]
                print(f"🔍 DEBUG: Best pitch data keys: {list(best_pitch_data.keys())}")
                
                # Parse JSON fields if they are stored as strings
                json_fields = ['perfect_conversation', 'score_improvement', 'overall_improvements']
                for field in json_fields:
                    if field in best_pitch_data and best_pitch_data[field]:
                        if isinstance(best_pitch_data[field], str):
                            try:
                                best_pitch_data[field] = json.loads(best_pitch_data[field])
                                print(f"✅ Parsed JSON field: {field}")
                            except json.JSONDecodeError as e:
                                print(f"⚠️ Failed to parse JSON field {field}: {e}")
                
                return best_pitch_data
            else:
                print(f"🔍 DEBUG: No best pitch found for conversation_id: {conversation_id}")
                return None
                
        except Exception as e:
            print(f"Error getting conversation best pitch: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # OPTIMIZED SUMMARY OPERATIONS
    def get_conversation_summary(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get conversation summary with analysis and best pitch data - Optimized"""
        try:
            start_time = time.time()
            
            # Use a single optimized query with joins if possible
            # For now, we'll optimize the existing approach
            result = self.supabase.table("conversation_summary").select(
                "conversation_id,conversation_title,conversation_created,analysis_score,best_pitch_exists"
            ).eq("user_id", user_id).order("conversation_created", desc=True).limit(limit).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation summary retrieved in {execution_time:.2f}ms")
            
            return result.data
        except Exception as e:
            print(f"Error getting conversation summary: {e}")
            return []
    
    # NEW OPTIMIZED METHODS FOR BETTER PERFORMANCE
    def get_complete_conversation_data_optimized(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get complete data for a conversation including analysis and best pitch - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Use a single query with joins to get all related data at once
            # This reduces 3 separate queries to 1
            result = self.supabase.rpc('get_complete_conversation_data', {
                'p_conversation_id': conversation_id,
                'p_user_id': user_id
            }).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Complete conversation data retrieved in {execution_time:.2f}ms")
            
            if result.data:
                return result.data[0]
            else:
                # Fallback to individual queries if RPC function doesn't exist
                return self._get_complete_conversation_data_fallback(conversation_id, user_id)
                
        except Exception as e:
            print(f"Error in optimized complete conversation data: {e}")
            # Fallback to individual queries
            return self._get_complete_conversation_data_fallback(conversation_id, user_id)
    
    def _get_complete_conversation_data_fallback(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Fallback method using individual queries"""
        try:
            start_time = time.time()
            
            # Get conversation
            conversation = self.get_conversation(conversation_id, user_id)
            if not conversation:
                return None
            
            # Get analysis
            analysis = self.get_conversation_analysis(conversation_id, user_id)
            
            # Get best pitch
            best_pitch = self.get_conversation_best_pitch(conversation_id, user_id)
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Fallback complete data retrieved in {execution_time:.2f}ms")
            
            return {
                "conversation": conversation,
                "analysis": analysis,
                "best_pitch": best_pitch
            }
        except Exception as e:
            print(f"Error in fallback complete conversation data: {e}")
            return None

    def get_all_conversations_optimized(self, user_id: str) -> List[Dict]:
        """Get all conversations for a user - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Use the service role client for database operations since we're using custom JWT auth
            client = self.supabase
            
            # Select only essential columns for better performance
            response = client.table('conversations').select(
                'id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status'
            ).eq('user_id', user_id).order('created_at', desc=True).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ {len(response.data)} conversations retrieved in {execution_time:.2f}ms")
            
            if response.data:
                return response.data
            else:
                return []
                
        except Exception as e:
            print(f"Error getting all conversations: {e}")
            return []

    def get_all_conversations_admin_optimized(self) -> List[Dict]:
        """Get all conversations for admin users with user information - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Use the service role client for database operations since we're using custom JWT auth
            client = self.supabase
            
            print("🔍 DEBUG: Starting admin conversations query...")
            
            # First, let's try a simple query without join to see if we get any conversations
            print("🔍 DEBUG: Testing simple query first...")
            simple_response = client.table('conversations').select('id,title,user_id').execute()
            print(f"🔍 DEBUG: Simple query returned {len(simple_response.data)} conversations")
            if simple_response.data:
                print(f"🔍 DEBUG: First conversation user_id: {simple_response.data[0].get('user_id')}")
            
            # Fetch conversations with agent and user information
            print("🔍 DEBUG: Fetching conversations with agent and user info...")
            conversations_response = client.table('conversations').select(
                'id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status,user_id,agent_id,agents(title,agent_key)'
            ).order('created_at', desc=True).execute()
            
            print(f"🔍 DEBUG: Conversations query returned {len(conversations_response.data)} conversations")
            
            # Fetch all users to create a lookup map
            print("🔍 DEBUG: Fetching users for lookup...")
            users_response = client.table('users').select('id,first_name,last_name,email').execute()
            print(f"🔍 DEBUG: Users query returned {len(users_response.data)} users")
            
            # Create a user lookup map
            users_map = {}
            for user in users_response.data:
                users_map[user['id']] = user
            
            print(f"🔍 DEBUG: Users map created with {len(users_map)} users")
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ {len(conversations_response.data)} conversations (admin) retrieved in {execution_time:.2f}ms")
            
            if conversations_response.data:
                # Process the data to include user name and agent information
                conversations = []
                for conv in conversations_response.data:
                    conversation = conv.copy()
                    
                    # Get user information from the lookup map
                    user_id = conv.get('user_id')
                    if user_id and user_id in users_map:
                        user = users_map[user_id]
                        first_name = user.get('first_name', '')
                        last_name = user.get('last_name', '')
                        email = user.get('email', '')
                        
                        # Create user name
                        if first_name or last_name:
                            user_name = f"{first_name} {last_name}".strip()
                        else:
                            user_name = email.split('@')[0] if email else 'Unknown User'
                        
                        conversation['user_name'] = user_name
                    else:
                        conversation['user_name'] = 'Unknown User'
                    
                    # Get agent information
                    agent_id = conv.get('agent_id')
                    agent_data = conv.get('agents')
                    if agent_id and agent_data:
                        conversation['agent_title'] = agent_data.get('title', 'Unknown Agent')
                        conversation['agent_key'] = agent_data.get('agent_key', 'unknown')
                    elif agent_id:
                        conversation['agent_title'] = f"Agent {agent_id[:8]}"
                        conversation['agent_key'] = 'unknown'
                    else:
                        conversation['agent_title'] = 'No Agent'
                        conversation['agent_key'] = 'none'
                    
                    conversations.append(conversation)
                
                return conversations
            else:
                return []
                
        except Exception as e:
            print(f"Error getting all conversations (admin): {e}")
            return []

    def get_conversation_by_id_optimized(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Use the service role client for database operations since we're using custom JWT auth
            client = self.supabase
            
            # Select necessary columns including transcript for analysis page
            response = client.table('conversations').select(
                'id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status,transcript,audio_data,audio_duration_seconds'
            ).eq('id', conversation_id).eq('user_id', user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation {conversation_id} retrieved in {execution_time:.2f}ms")
            
            if response.data:
                conversation_data = response.data[0]
                
                # Parse transcript if it's stored as a JSON string
                if 'transcript' in conversation_data and conversation_data['transcript']:
                    if isinstance(conversation_data['transcript'], str):
                        try:
                            conversation_data['transcript'] = json.loads(conversation_data['transcript'])
                            print(f"✅ Parsed transcript JSON")
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Failed to parse transcript JSON: {e}")
                            # Keep as string if parsing fails
                
                return conversation_data
            else:
                return None
                
        except Exception as e:
            print(f"Error getting conversation by ID: {e}")
            return None

    def get_conversation_by_id_admin(self, conversation_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID - ADMIN VERSION (no user_id filter)"""
        try:
            start_time = time.time()
            
            # Use the service role client for database operations
            client = self.supabase
            
            # Select necessary columns including transcript for analysis page
            response = client.table('conversations').select(
                'id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status,transcript,audio_data,audio_duration_seconds,user_id'
            ).eq('id', conversation_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Admin: Conversation {conversation_id} retrieved in {execution_time:.2f}ms")
            
            if response.data:
                conversation_data = response.data[0]
                
                # Parse transcript if it's stored as a JSON string
                if 'transcript' in conversation_data and conversation_data['transcript']:
                    if isinstance(conversation_data['transcript'], str):
                        try:
                            conversation_data['transcript'] = json.loads(conversation_data['transcript'])
                            print(f"✅ Admin: Parsed transcript JSON")
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Admin: Failed to parse transcript JSON: {e}")
                            # Keep as string if parsing fails
                
                return conversation_data
            else:
                return None
                
        except Exception as e:
            print(f"Error getting conversation by ID (admin): {e}")
            return None

    def get_analysis_by_conversation_id_optimized(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get analysis data for a specific conversation - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Use the service role client for database operations since we're using custom JWT auth
            client = self.supabase
            
            print(f"🔍 DEBUG: Fetching analysis for conversation_id: {conversation_id}, user_id: {user_id}")
            
            # Select all necessary columns for complete analysis data
            response = client.table('analysis').select(
                'id,conversation_id,overall_score,key_metrics,strengths,improvements,created_at,session_info,voice_delivery_analysis,sales_skills_assessment,sales_process_flow,detailed_feedback,recommendations'
            ).eq('conversation_id', conversation_id).eq('user_id', user_id).execute()
            
            print(f"🔍 DEBUG: Raw response data: {response.data}")
            print(f"🔍 DEBUG: Response count: {len(response.data) if response.data else 0}")
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Analysis for conversation {conversation_id} retrieved in {execution_time:.2f}ms")
            
            if response.data:
                analysis_data = response.data[0]
                print(f"🔍 DEBUG: Analysis data keys: {list(analysis_data.keys())}")
                
                # Parse JSON fields if they are stored as strings
                json_fields = ['overall_score', 'key_metrics', 'strengths', 'improvements', 
                              'session_info', 'voice_delivery_analysis', 'sales_skills_assessment', 
                              'sales_process_flow', 'detailed_feedback', 'recommendations']
                
                for field in json_fields:
                    if field in analysis_data and analysis_data[field]:
                        print(f"🔍 DEBUG: Field {field} type: {type(analysis_data[field])}")
                        print(f"🔍 DEBUG: Field {field} value: {analysis_data[field]}")
                        if isinstance(analysis_data[field], str):
                            try:
                                analysis_data[field] = json.loads(analysis_data[field])
                                print(f"✅ Parsed JSON field: {field}")
                            except json.JSONDecodeError as e:
                                print(f"⚠️ Failed to parse JSON field {field}: {e}")
                                # Keep as string if parsing fails
                
                return analysis_data
            else:
                print(f"🔍 DEBUG: No analysis data found for conversation_id: {conversation_id}")
                return None
                
        except Exception as e:
            print(f"Error getting analysis by conversation ID: {e}")
            return None

    def get_analysis_by_conversation_id_admin(self, conversation_id: str) -> Optional[Dict]:
        """Get analysis data for a specific conversation - ADMIN VERSION (no user_id filter)"""
        try:
            start_time = time.time()
            
            # Use the service role client for database operations
            client = self.supabase
            
            print(f"🔍 DEBUG: Admin: Fetching analysis for conversation_id: {conversation_id}")
            
            # Select all necessary columns for complete analysis data
            response = client.table('analysis').select(
                'id,conversation_id,overall_score,key_metrics,strengths,improvements,created_at,session_info,voice_delivery_analysis,sales_skills_assessment,sales_process_flow,detailed_feedback,recommendations,user_id'
            ).eq('conversation_id', conversation_id).execute()
            
            print(f"🔍 DEBUG: Admin: Raw response data: {response.data}")
            print(f"🔍 DEBUG: Admin: Response count: {len(response.data) if response.data else 0}")
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Admin: Analysis for conversation {conversation_id} retrieved in {execution_time:.2f}ms")
            
            if response.data:
                analysis_data = response.data[0]
                print(f"🔍 DEBUG: Admin: Analysis data keys: {list(analysis_data.keys())}")
                
                # Parse JSON fields if they are stored as strings
                json_fields = ['overall_score', 'key_metrics', 'strengths', 'improvements', 
                              'session_info', 'voice_delivery_analysis', 'sales_skills_assessment', 
                              'sales_process_flow', 'detailed_feedback', 'recommendations']
                
                for field in json_fields:
                    if field in analysis_data and analysis_data[field]:
                        print(f"🔍 DEBUG: Admin: Field {field} type: {type(analysis_data[field])}")
                        print(f"🔍 DEBUG: Admin: Field {field} value: {analysis_data[field]}")
                        if isinstance(analysis_data[field], str):
                            try:
                                analysis_data[field] = json.loads(analysis_data[field])
                                print(f"✅ Admin: Parsed JSON field: {field}")
                            except json.JSONDecodeError as e:
                                print(f"⚠️ Admin: Failed to parse JSON field {field}: {e}")
                                # Keep as string if parsing fails
                
                return analysis_data
            else:
                print(f"🔍 DEBUG: Admin: No analysis data found for conversation_id: {conversation_id}")
                return None
                
        except Exception as e:
            print(f"Error getting analysis by conversation ID (admin): {e}")
            return None

    # LEGACY METHODS (keeping for backward compatibility)
    def get_complete_conversation_data(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get complete data for a conversation including analysis and best pitch - LEGACY"""
        return self.get_complete_conversation_data_optimized(conversation_id, user_id)

    def get_all_conversations(self, user_id: str) -> List[Dict]:
        """Get all conversations for a user - LEGACY"""
        return self.get_all_conversations_optimized(user_id)

    def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID - LEGACY"""
        return self.get_conversation_by_id_optimized(conversation_id, user_id)

    def get_analysis_by_conversation_id(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get analysis data for a specific conversation - LEGACY"""
        return self.get_analysis_by_conversation_id_optimized(conversation_id, user_id)

    # AGENT OPERATIONS
    def get_all_agents(self) -> List[Dict]:
        """Get all active agents from the database"""
        try:
            start_time = time.time()
            
            # Use service role client for agent operations to bypass RLS
            service_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
            
            result = service_client.table("agents").select(
                "id,agent_key,title,icon,icon_class,type,guidelines,difficulty,is_active"
            ).eq("is_active", True).order("title").execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ {len(result.data)} agents retrieved in {execution_time:.2f}ms")
            
            return result.data
        except Exception as e:
            print(f"Error getting agents: {e}")
            return []
    
    def get_agent_by_key(self, agent_key: str) -> Optional[Dict]:
        """Get a specific agent by its key"""
        try:
            start_time = time.time()
            
            # Use service role client for agent operations to bypass RLS
            service_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
            
            result = service_client.table("agents").select(
                "id,agent_key,title,icon,icon_class,type,guidelines,difficulty,is_active"
            ).eq("agent_key", agent_key).eq("is_active", True).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Agent {agent_key} retrieved in {execution_time:.2f}ms")
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting agent by key: {e}")
            return None
    
    def get_agents_by_type(self, agent_type: str) -> List[Dict]:
        """Get all agents of a specific type"""
        try:
            start_time = time.time()
            
            result = self.supabase.table("agents").select(
                "id,agent_key,title,icon,icon_class,type,guidelines,difficulty,is_active"
            ).eq("type", agent_type).eq("is_active", True).order("title").execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ {len(result.data)} agents of type {agent_type} retrieved in {execution_time:.2f}ms")
            
            return result.data
        except Exception as e:
            print(f"Error getting agents by type: {e}")
            return []
    
    def get_agents_by_difficulty(self, difficulty: str) -> List[Dict]:
        """Get all agents of a specific difficulty level"""
        try:
            start_time = time.time()
            
            result = self.supabase.table("agents").select(
                "id,agent_key,title,icon,icon_class,type,guidelines,difficulty,is_active"
            ).eq("difficulty", difficulty).eq("is_active", True).order("title").execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ {len(result.data)} agents of difficulty {difficulty} retrieved in {execution_time:.2f}ms")
            
            return result.data
        except Exception as e:
            print(f"Error getting agents by difficulty: {e}")
            return []

    def get_conversation_stats(self) -> Dict:
        """Get conversation statistics for admin dashboard"""
        try:
            start_time = time.time()
            
            # Use service role client for admin operations
            service_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
            
            # Get total recordings count
            conversations_result = service_client.table("conversations").select("id", count="exact").execute()
            total_recordings = conversations_result.count if conversations_result.count else 0
            
            # Get average role-play score from analysis table
            analysis_result = service_client.table("analysis").select("overall_score").execute()
            scores = []
            if analysis_result.data:
                for analysis in analysis_result.data:
                    overall_score = analysis.get('overall_score')
                    if overall_score:
                        if isinstance(overall_score, str):
                            try:
                                overall_score = json.loads(overall_score)
                            except json.JSONDecodeError:
                                continue
                        if isinstance(overall_score, dict) and 'percentage' in overall_score:
                            scores.append(overall_score['percentage'])
            
            avg_score = sum(scores) / len(scores) if scores else 0
            
            # Get total practice minutes
            duration_result = service_client.table("conversations").select("duration_seconds").execute()
            total_minutes = 0
            if duration_result.data:
                total_minutes = sum(conv.get('duration_seconds', 0) for conv in duration_result.data) // 60
            
            # Get recordings with 80%+ score
            high_score_count = len([score for score in scores if score >= 80])
            high_score_percentage = (high_score_count / total_recordings * 100) if total_recordings > 0 else 0
            
            # Get top 5 role-plays (most used agents) using proper agent relationships
            conversations_with_agents = service_client.table("conversations").select(
                "agent_id, agents(title)"
            ).execute()
            
            role_play_counts = {}
            if conversations_with_agents.data:
                for conv in conversations_with_agents.data:
                    agent_id = conv.get('agent_id')
                    agent_data = conv.get('agents')
                    
                    if agent_id and agent_data:
                        agent_title = agent_data.get('title', 'Unknown Agent')
                        role_play_counts[agent_title] = role_play_counts.get(agent_title, 0) + 1
                    elif agent_id:
                        # Fallback: use agent_id if agent data is not available
                        role_play_counts[f"Agent {agent_id[:8]}"] = role_play_counts.get(f"Agent {agent_id[:8]}", 0) + 1
            
            # Sort and get top 5
            top_role_plays = sorted(role_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation stats retrieved in {execution_time:.2f}ms")
            
            return {
                'total_recordings': total_recordings,
                'avg_role_play_score': round(avg_score, 1),
                'total_practice_minutes': total_minutes,
                'recordings_80_plus_score': high_score_count,
                'recordings_80_plus_percentage': round(high_score_percentage, 1),
                'top_role_plays': top_role_plays
            }
            
        except Exception as e:
            print(f"Error getting conversation stats: {e}")
            return {
                'total_recordings': 0,
                'avg_role_play_score': 0,
                'total_practice_minutes': 0,
                'recordings_80_plus_score': 0,
                'recordings_80_plus_percentage': 0,
                'top_role_plays': []
            }
    

# Utility functions for audio handling
def encode_audio_to_base64(audio_bytes: bytes) -> str:
    """Convert audio bytes to base64 string"""
    return base64.b64encode(audio_bytes).decode('utf-8')

def decode_audio_from_base64(base64_string: str) -> bytes:
    """Convert base64 string back to audio bytes"""
    return base64.b64decode(base64_string.encode('utf-8'))

# Example usage functions
def example_save_conversation_with_analysis():
    """Example of how to save a complete conversation with analysis and best pitch"""
    db = DatabaseManager()
    
    # Example conversation data
    conversation_data = {
        "title": "Sales Call with Mike",
        "duration_seconds": 300,
        "conversation_history": [
            {"user": "Hi, I'm Mike from Global Trade Solutions", "assistant": "Hello Mike! How can I help you today?", "timestamp": "2024-01-15T10:00:00Z"},
            {"user": "I'm looking for supplier discovery tools", "assistant": "Great! Let me tell you about our platform...", "timestamp": "2024-01-15T10:01:00Z"}
        ],
        "transcript": [
            {"sender": "user", "text": "Hi, I'm Mike from Global Trade Solutions", "time": "10:00:00"},
            {"sender": "assistant", "text": "Hello Mike! How can I help you today?", "time": "10:00:05"}
        ]
    }
    
    # Example analysis data
    analysis_data = {
        "overall_score": {"percentage": 75, "grade": "B+"},
        "key_metrics": {"clarity_score": 80, "engagement_score": 70},
        "voice_delivery_analysis": {"tone": 85, "pace": 75},
        "sales_skills_assessment": {"questioning": 4, "objection_handling": 3},
        "strengths": ["Good opening", "Clear communication"],
        "improvements": ["Ask more probing questions", "Handle objections better"]
    }
    
    # Example best pitch data
    best_pitch_data = {
        "perfect_conversation": [
            {"user": "Hi, I'm Mike from Global Trade Solutions", "assistant": "Hello Mike! I'd love to learn about your supplier discovery needs. What specific challenges are you facing?", "timestamp": "2024-01-15T10:00:00Z"}
        ],
        "score_improvement": {"original_score": 75, "perfect_score": 90, "improvement": 15}
    }
    
    # Save conversation
    user_id = "example-user-id"
    conv_result = db.save_conversation(user_id, conversation_data)
    
    if conv_result["success"]:
        conversation_id = conv_result["conversation_id"]
        
        # Save analysis
        analysis_result = db.save_analysis(user_id, conversation_id, analysis_data)
        
        if analysis_result["success"]:
            analysis_id = analysis_result["analysis_id"]
            
            # Save best pitch
            best_pitch_result = db.save_best_pitch(user_id, conversation_id, analysis_id, best_pitch_data)
            
            print(f"Complete data saved: Conversation={conversation_id}, Analysis={analysis_id}, Best Pitch={best_pitch_result.get('best_pitch_id')}")
    
    return conv_result 