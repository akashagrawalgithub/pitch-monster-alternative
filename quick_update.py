#!/usr/bin/env python3
"""
Quick one-liner script to update user role
"""

from supabase import create_client
from datetime import datetime

# Initialize client
supabase = create_client(
    "https://hblifaxxsqkgwzcwxzxo.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhibGlmYXh4c3FrZ3d6Y3d4enhvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTM3MDI3MSwiZXhwIjoyMDcwOTQ2MjcxfQ.3O1-uAb1W2xud9L-ciePHFxUCKxNbuCklSVtdVWvy8w"
)

# Update user role
result = supabase.table("users").update({
    "role": "admin",
    "updated_at": datetime.now().isoformat()
}).eq("email", "akash242018@gmail.com").execute()

print("✅ User role updated to admin!" if result.data else "❌ Failed to update user role")
