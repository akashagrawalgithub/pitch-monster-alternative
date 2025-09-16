#!/usr/bin/env python3
"""
Script to update user role from user to admin
Usage: python update_user_role.py
"""

import os
import sys
from supabase import create_client, Client
from datetime import datetime

# Supabase configuration
SUPABASE_URL = "https://hblifaxxsqkgwzcwxzxo.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhibGlmYXh4c3FrZ3d6Y3d4enhvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTM3MDI3MSwiZXhwIjoyMDcwOTQ2MjcxfQ.3O1-uAb1W2xud9L-ciePHFxUCKxNbuCklSVtdVWvy8w"

def update_user_role():
    """Update akash242018@gmail.com from user to admin"""
    try:
        # Initialize Supabase client with service role
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        # Update user role
        result = supabase.table("users").update({
            "role": "admin",
            "updated_at": datetime.now().isoformat()
        }).eq("email", "akash242018@gmail.com").execute()
        
        if result.data:
            user = result.data[0]
            print(f"✅ SUCCESS: User {user['email']} role updated to {user['role']}")
            print(f"   User ID: {user['id']}")
            print(f"   Name: {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"   Active: {user.get('is_active', True)}")
            return True
        else:
            print("❌ ERROR: No user found with email akash242018@gmail.com")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to update user role: {e}")
        return False

def verify_user_role():
    """Verify the user role was updated"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        result = supabase.table("users").select("*").eq("email", "akash242018@gmail.com").execute()
        
        if result.data:
            user = result.data[0]
            print(f"\n🔍 VERIFICATION:")
            print(f"   Email: {user['email']}")
            print(f"   Role: {user['role']}")
            print(f"   Active: {user.get('is_active', True)}")
            print(f"   Updated: {user.get('updated_at', 'N/A')}")
            return user['role'] == 'admin'
        else:
            print("❌ User not found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to verify user: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Updating user role for akash242018@gmail.com...")
    print("=" * 50)
    
    # Update the role
    success = update_user_role()
    
    if success:
        # Verify the update
        print("\n" + "=" * 50)
        verify_success = verify_user_role()
        
        if verify_success:
            print("\n🎉 SUCCESS: User is now an admin!")
        else:
            print("\n⚠️ WARNING: Update may not have worked correctly")
    else:
        print("\n❌ FAILED: Could not update user role")
        sys.exit(1)
