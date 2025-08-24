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
        # For now, we'll use the anon key and handle RLS differently
        pass
    
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
            result = self.supabase.table("conversations").insert(conversation_record).execute()
            
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
            
            # Use the complete best pitch data as provided
            best_pitch_record = best_pitch_data.copy()
            best_pitch_record["conversation_id"] = conversation_id
            best_pitch_record["analysis_id"] = analysis_id
            best_pitch_record["user_id"] = user_id
            
            # Ensure required fields are present
            if "created_at" not in best_pitch_record:
                best_pitch_record["created_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("best_pitch").insert(best_pitch_record).execute()
            
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
            
            result = self.supabase.table("best_pitch").select(
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
            
            result = self.supabase.table("best_pitch").select(
                "id,conversation_id,analysis_id,perfect_conversation,score_improvement,created_at"
            ).eq("conversation_id", conversation_id).eq("user_id", user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation best pitch retrieved in {execution_time:.2f}ms")
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting conversation best pitch: {e}")
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
            
            # Select only essential columns for better performance
            response = self.supabase.table('conversations').select(
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

    def get_conversation_by_id_optimized(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Select necessary columns including transcript for analysis page
            response = self.supabase.table('conversations').select(
                'id,title,session_id,duration_seconds,total_exchanges,created_at,updated_at,status,transcript,audio_data,audio_duration_seconds'
            ).eq('id', conversation_id).eq('user_id', user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Conversation {conversation_id} retrieved in {execution_time:.2f}ms")
            
            if response.data:
                return response.data[0]
            else:
                return None
                
        except Exception as e:
            print(f"Error getting conversation by ID: {e}")
            return None

    def get_analysis_by_conversation_id_optimized(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get analysis data for a specific conversation - OPTIMIZED VERSION"""
        try:
            start_time = time.time()
            
            # Select all necessary columns for complete analysis data
            response = self.supabase.table('analysis').select(
                'id,conversation_id,overall_score,key_metrics,strengths,improvements,created_at,session_info,voice_delivery_analysis,sales_skills_assessment,sales_process_flow,detailed_feedback,recommendations'
            ).eq('conversation_id', conversation_id).eq('user_id', user_id).execute()
            
            execution_time = (time.time() - start_time) * 1000
            print(f"✅ Analysis for conversation {conversation_id} retrieved in {execution_time:.2f}ms")
            
            if response.data:
                return response.data[0]
            else:
                return None
                
        except Exception as e:
            print(f"Error getting analysis by conversation ID: {e}")
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