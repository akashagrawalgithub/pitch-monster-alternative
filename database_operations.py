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

# Supabase configuration (from your app.py)
SUPABASE_URL = "https://hblifaxxsqkgwzcwxzxo.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhibGlmYXh4c3FrZ3d6Y3d4enhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUzNzAyNzEsImV4cCI6MjA3MDk0NjI3MX0.nbLnB8IIWjLvHA7De1LZLveY5UnS_bP8UcfNLd_rPq0"

class DatabaseManager:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    def get_current_user_id(self, access_token: str) -> Optional[str]:
        """Get current user ID from access token"""
        try:
            user = self.supabase.auth.get_user(access_token)
            return user.id if user else None
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
    
    # CONVERSATION OPERATIONS
    def save_conversation(self, user_id: str, conversation_data: Dict, audio_data: str = None) -> Dict:
        """Save a new conversation to the database"""
        try:
            # Prepare conversation data
            conversation_record = {
                "user_id": user_id,
                "session_id": str(uuid.uuid4()),
                "title": conversation_data.get("title", "Sales Conversation"),
                "duration_seconds": conversation_data.get("duration_seconds", 0),
                "total_exchanges": len(conversation_data.get("conversation_history", [])),
                "full_conversation": conversation_data.get("conversation_history", []),
                "transcript": conversation_data.get("transcript", []),
                "audio_data": audio_data,  # Base64 encoded audio
                "audio_format": "pcm_f32le",
                "sample_rate": 44100,
                "audio_duration_seconds": conversation_data.get("audio_duration", 0),
                "user_agent": conversation_data.get("user_agent"),
                "ip_address": conversation_data.get("ip_address"),
                "status": "active",
                "tags": conversation_data.get("tags", []),
                "notes": conversation_data.get("notes")
            }
            
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
        """Save analysis results to the database"""
        try:
            analysis_record = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "analysis_version": "1.0",
                "model_used": "gpt-4o-mini",
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
                "status": "completed"
            }
            
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
        """Save best pitch results to the database"""
        try:
            best_pitch_record = {
                "conversation_id": conversation_id,
                "analysis_id": analysis_id,
                "user_id": user_id,
                "perfect_conversation": best_pitch_data.get("perfect_conversation", []),
                "original_conversation": best_pitch_data.get("original_conversation", []),
                "score_improvement": best_pitch_data.get("score_improvement", {}),
                "overall_improvements": best_pitch_data.get("overall_improvements", {}),
                "model_used": "gpt-4o-mini",
                "generation_version": "1.0",
                "key_changes": best_pitch_data.get("key_changes", []),
                "improvement_areas": best_pitch_data.get("improvement_areas", []),
                "best_practices_applied": best_pitch_data.get("best_practices_applied", []),
                "status": "completed"
            }
            
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