"""
Database operations for Voice Web Chat Application
Handles CRUD operations for conversations, analysis, and best_pitch tables
"""

from supabase import create_client, Client
from datetime import datetime
import json
import base64
from typing import Dict, List, Optional, Any
import uuid
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

class DatabaseManager:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self.current_token = None
    
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
    
    # CONVERSATION OPERATIONS
    def save_conversation(self, user_id: str, conversation_data: Dict) -> Dict:
        """Save a new conversation to the database with complete schema data"""
        try:
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
        """Get a specific conversation by ID"""
        try:
            result = self.supabase.table("conversations").select("*").eq("id", conversation_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None
    
    def get_user_conversations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get all conversations for a user"""
        try:
            result = self.supabase.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            print(f"Error getting user conversations: {e}")
            return []
    
    def update_conversation(self, conversation_id: str, user_id: str, updates: Dict) -> bool:
        """Update a conversation"""
        try:
            result = self.supabase.table("conversations").update(updates).eq("id", conversation_id).eq("user_id", user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating conversation: {e}")
            return False
    
    def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Delete a conversation (will cascade to analysis and best_pitch)"""
        try:
            result = self.supabase.table("conversations").delete().eq("id", conversation_id).eq("user_id", user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    # ANALYSIS OPERATIONS
    def save_analysis(self, user_id: str, conversation_id: str, analysis_data: Dict) -> Dict:
        """Save analysis results to the database with complete schema data"""
        try:
            # Use the complete analysis data as provided
            analysis_record = analysis_data.copy()
            analysis_record["conversation_id"] = conversation_id
            analysis_record["user_id"] = user_id
            
            # Ensure required fields are present
            if "created_at" not in analysis_record:
                analysis_record["created_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("analysis").insert(analysis_record).execute()
            
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
        """Get a specific analysis by ID"""
        try:
            result = self.supabase.table("analysis").select("*").eq("id", analysis_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting analysis: {e}")
            return None
    
    def get_conversation_analysis(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get analysis for a specific conversation"""
        try:
            result = self.supabase.table("analysis").select("*").eq("conversation_id", conversation_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting conversation analysis: {e}")
            return None
    
    # BEST PITCH OPERATIONS
    def save_best_pitch(self, user_id: str, conversation_id: str, analysis_id: str, best_pitch_data: Dict) -> Dict:
        """Save best pitch results to the database with complete schema data"""
        try:
            # Use the complete best pitch data as provided
            best_pitch_record = best_pitch_data.copy()
            best_pitch_record["conversation_id"] = conversation_id
            best_pitch_record["analysis_id"] = analysis_id
            best_pitch_record["user_id"] = user_id
            
            # Ensure required fields are present
            if "created_at" not in best_pitch_record:
                best_pitch_record["created_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("best_pitch").insert(best_pitch_record).execute()
            
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
        """Get a specific best pitch by ID"""
        try:
            result = self.supabase.table("best_pitch").select("*").eq("id", best_pitch_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting best pitch: {e}")
            return None
    
    def get_conversation_best_pitch(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get best pitch for a specific conversation"""
        try:
            result = self.supabase.table("best_pitch").select("*").eq("conversation_id", conversation_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting conversation best pitch: {e}")
            return None
    
    # SUMMARY OPERATIONS
    def get_conversation_summary(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get conversation summary with analysis and best pitch data"""
        try:
            result = self.supabase.table("conversation_summary").select("*").eq("user_id", user_id).order("conversation_created", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            print(f"Error getting conversation summary: {e}")
            return []
    
    def get_complete_conversation_data(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get complete data for a conversation including analysis and best pitch"""
        try:
            # Get conversation
            conversation = self.get_conversation(conversation_id, user_id)
            if not conversation:
                return None
            
            # Get analysis
            analysis = self.get_conversation_analysis(conversation_id, user_id)
            
            # Get best pitch
            best_pitch = self.get_conversation_best_pitch(conversation_id, user_id)
            
            return {
                "conversation": conversation,
                "analysis": analysis,
                "best_pitch": best_pitch
            }
        except Exception as e:
            print(f"Error getting complete conversation data: {e}")
            return None

    def get_all_conversations(self, user_id: str) -> List[Dict]:
        """Get all conversations for a user"""
        try:
            response = self.supabase.table('conversations').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            
            if response.data:
                print(f"✅ Retrieved {len(response.data)} conversations for user {user_id}")
                return response.data
            else:
                print(f"✅ No conversations found for user {user_id}")
                return []
                
        except Exception as e:
            print(f"Error getting all conversations: {e}")
            return []

    def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID"""
        try:
            response = self.supabase.table('conversations').select('*').eq('id', conversation_id).eq('user_id', user_id).execute()
            
            if response.data:
                print(f"✅ Retrieved conversation {conversation_id}")
                return response.data[0]
            else:
                print(f"❌ Conversation {conversation_id} not found")
                return None
                
        except Exception as e:
            print(f"Error getting conversation by ID: {e}")
            return None

    def get_analysis_by_conversation_id(self, conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get analysis data for a specific conversation"""
        try:
            response = self.supabase.table('analysis').select('*').eq('conversation_id', conversation_id).eq('user_id', user_id).execute()
            
            if response.data:
                print(f"✅ Retrieved analysis for conversation {conversation_id}")
                return response.data[0]
            else:
                print(f"❌ No analysis found for conversation {conversation_id}")
                return None
                
        except Exception as e:
            print(f"Error getting analysis by conversation ID: {e}")
            return None

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