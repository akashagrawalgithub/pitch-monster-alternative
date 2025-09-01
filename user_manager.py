from typing import Dict, Optional, List
from supabase import create_client, Client
import os
import bcrypt
import jwt
from datetime import datetime, timedelta

class UserManager:
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        
        # Initialize Supabase client with service role for admin operations
        self.supabase: Client = create_client(self.supabase_url, self.supabase_service_key)
        
        # JWT secret (in production, use environment variable)
        self.jwt_secret = os.environ.get("JWT_SECRET")
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_user(self, email: str, password: str, first_name: str = None, last_name: str = None, role: str = 'user') -> Optional[Dict]:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = self.get_user_by_email(email)
            if existing_user:
                return None
            
            # Hash the password
            password_hash = self.hash_password(password)
            
            # Create user
            result = self.supabase.table("users").insert({
                "email": email,
                "password_hash": password_hash,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "is_active": True
            }).execute()
            
            if result.data:
                user = result.data[0]
                # Don't return password hash
                user.pop('password_hash', None)
                return user
            
            return None
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate a user and return user data with token"""
        try:
            # Get user by email
            user = self.get_user_by_email(email)
            if not user:
                return None
            
            # Check if user is active
            if not user.get('is_active', True):
                return None
            
            # Verify password
            if not self.verify_password(password, user['password_hash']):
                return None
            
            # Update last login
            self.update_last_login(user['id'])
            
            # Generate JWT token
            token = self.generate_token(user['id'], user['email'], user['role'])
            
            # Return user data without password hash
            user_data = user.copy()
            user_data.pop('password_hash', None)
            user_data['token'] = token
            
            return user_data
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            result = self.supabase.table("users").select("*").eq("email", email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            result = self.supabase.table("users").select("*").eq("id", user_id).execute()
            if result.data:
                user = result.data[0]
                user.pop('password_hash', None)
                return user
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        try:
            result = self.supabase.table("users").update({
                "last_login": datetime.now().isoformat()
            }).eq("id", user_id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error updating last login: {e}")
            return False
    
    def generate_token(self, user_id: str, email: str, role: str) -> str:
        """Generate JWT token"""
        payload = {
            'sub': user_id,  # Required subject claim
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=7)  # 7 days expiry
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            # Ensure sub claim exists and use it as user_id if user_id is not present
            if 'sub' in payload and 'user_id' not in payload:
                payload['user_id'] = payload['sub']
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None
    
    def is_admin(self, user_id: str) -> bool:
        """Check if user is admin"""
        try:
            user = self.get_user_by_id(user_id)
            return user and user.get('role') == 'admin' and user.get('is_active', True)
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False
    
    def get_all_users(self, admin_user_id: str) -> List[Dict]:
        """Get all users (admin only)"""
        try:
            # Check if requesting user is admin
            if not self.is_admin(admin_user_id):
                return []
            
            result = self.supabase.table("users").select(
                "id,email,first_name,last_name,role,is_active,last_login,created_at,updated_at"
            ).order("created_at", desc=True).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    def update_user_role(self, target_user_id: str, new_role: str, admin_user_id: str) -> bool:
        """Update user role (admin only)"""
        try:
            # Check if requesting user is admin
            if not self.is_admin(admin_user_id):
                return False
            
            # Validate role
            if new_role not in ['admin', 'user']:
                return False
            
            result = self.supabase.table("users").update({
                "role": new_role,
                "updated_at": datetime.now().isoformat()
            }).eq("id", target_user_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False
    
    def deactivate_user(self, target_user_id: str, admin_user_id: str) -> bool:
        """Deactivate user (admin only)"""
        try:
            # Check if requesting user is admin
            if not self.is_admin(admin_user_id):
                return False
            
            result = self.supabase.table("users").update({
                "is_active": False,
                "updated_at": datetime.now().isoformat()
            }).eq("id", target_user_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            print(f"Error deactivating user: {e}")
            return False
    
    def activate_user(self, target_user_id: str, admin_user_id: str) -> bool:
        """Activate user (admin only)"""
        try:
            # Check if requesting user is admin
            if not self.is_admin(admin_user_id):
                return False
            
            result = self.supabase.table("users").update({
                "is_active": True,
                "updated_at": datetime.now().isoformat()
            }).eq("id", target_user_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            print(f"Error activating user: {e}")
            return False
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Get current user
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            # Get user with password hash
            result = self.supabase.table("users").select("*").eq("id", user_id).execute()
            if not result.data:
                return False
            
            user_with_hash = result.data[0]
            
            # Verify current password
            if not self.verify_password(current_password, user_with_hash['password_hash']):
                return False
            
            # Hash new password
            new_password_hash = self.hash_password(new_password)
            
            # Update password
            update_result = self.supabase.table("users").update({
                "password_hash": new_password_hash,
                "updated_at": datetime.now().isoformat()
            }).eq("id", user_id).execute()
            
            return bool(update_result.data)
            
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
    
    def get_user_stats(self, admin_user_id: str) -> Dict:
        """Get user statistics (admin only)"""
        try:
            if not self.is_admin(admin_user_id):
                return {}
            
            result = self.supabase.table("users").select("*").execute()
            users = result.data if result.data else []
            
            total_users = len(users)
            active_users = len([u for u in users if u.get('is_active', True)])
            admin_users = len([u for u in users if u.get('role') == 'admin'])
            regular_users = len([u for u in users if u.get('role') == 'user'])
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'admin_users': admin_users,
                'regular_users': regular_users
            }
            
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {}

# Global instance
user_manager = UserManager() 