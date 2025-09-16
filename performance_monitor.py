#!/usr/bin/env python3
"""
Performance monitoring script to track AI response times
"""

import time
import requests
import json

def test_ai_response_time():
    """Test AI response time with a sample message"""
    url = "http://localhost:5000/chat_stream"
    payload = {
        "message": "Hello, how are you?",
        "agent_type": "discovery-call",
        "session_id": "test_session"
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=10)
        
        if response.status_code == 200:
            first_chunk_time = None
            total_response = ""
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        if first_chunk_time is None:
                            first_chunk_time = time.time() - start_time
                        
                        try:
                            data = json.loads(line_str[6:])
                            if 'reply' in data:
                                total_response += data['reply']
                        except:
                            pass
            
            total_time = time.time() - start_time
            
            print(f"🚀 Performance Test Results:")
            print(f"   First chunk time: {first_chunk_time:.2f}s")
            print(f"   Total response time: {total_time:.2f}s")
            print(f"   Response length: {len(total_response)} chars")
            print(f"   Status: {'✅ FAST' if first_chunk_time < 1.0 else '⚠️ SLOW'}")
            
            return first_chunk_time, total_time
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    print("🔍 Testing AI Response Performance...")
    print("=" * 40)
    
    first_chunk, total_time = test_ai_response_time()
    
    if first_chunk:
        if first_chunk < 0.5:
            print("\n🎉 EXCELLENT: AI responding very fast!")
        elif first_chunk < 1.0:
            print("\n✅ GOOD: AI responding at good speed")
        else:
            print("\n⚠️ SLOW: AI response needs optimization")
    else:
        print("\n❌ FAILED: Could not test performance")
