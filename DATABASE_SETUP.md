# Database Setup for Voice Web Chat Application

This document explains how to set up and use the Supabase database for your voice web chat application.

## Database Schema Overview

The application uses three main tables:

1. **`conversations`** - Stores conversation data, audio, and metadata
2. **`analysis`** - Stores analysis results linked to conversations
3. **`best_pitch`** - Stores perfect pitch versions and improvements

## Setup Instructions

### 1. Create Database Tables

1. Go to your Supabase project dashboard
2. Navigate to the SQL Editor
3. Copy and paste the entire contents of `database_schema.sql`
4. Execute the SQL script

This will create:
- All three tables with proper relationships
- Indexes for better performance
- Row Level Security (RLS) policies
- A summary view for easy querying
- Automatic timestamp updates

### 2. Table Structure Details

#### Conversations Table
```sql
- id: UUID (Primary Key)
- user_id: UUID (References auth.users)
- session_id: UUID
- created_at: Timestamp
- updated_at: Timestamp
- title: VARCHAR(255)
- duration_seconds: INTEGER
- total_exchanges: INTEGER
- full_conversation: JSONB (Array of conversation exchanges)
- transcript: JSONB (Array of transcript entries)
- audio_data: TEXT (Base64 encoded audio)
- audio_format: VARCHAR(50)
- sample_rate: INTEGER
- audio_duration_seconds: DECIMAL
- user_agent: TEXT
- ip_address: INET
- status: VARCHAR(50)
- tags: TEXT[]
- notes: TEXT
```

#### Analysis Table
```sql
- id: UUID (Primary Key)
- conversation_id: UUID (References conversations)
- user_id: UUID (References auth.users)
- created_at: Timestamp
- analysis_version: VARCHAR(20)
- model_used: VARCHAR(100)
- session_info: JSONB
- overall_score: JSONB
- key_metrics: JSONB
- voice_delivery_analysis: JSONB
- sales_skills_assessment: JSONB
- sales_process_flow: JSONB
- strengths: JSONB
- improvements: JSONB
- detailed_feedback: JSONB
- recommendations: JSONB
- status: VARCHAR(50)
```

#### Best Pitch Table
```sql
- id: UUID (Primary Key)
- conversation_id: UUID (References conversations)
- analysis_id: UUID (References analysis)
- user_id: UUID (References auth.users)
- created_at: Timestamp
- perfect_conversation: JSONB
- original_conversation: JSONB
- score_improvement: JSONB
- overall_improvements: JSONB
- model_used: VARCHAR(100)
- generation_version: VARCHAR(20)
- key_changes: JSONB
- improvement_areas: JSONB
- best_practices_applied: JSONB
- status: VARCHAR(50)
```

### 3. Integration with Flask App

#### Import the Database Manager
```python
from database_operations import DatabaseManager, encode_audio_to_base64

# Initialize database manager
db = DatabaseManager()
```

#### Save a Complete Conversation Flow
```python
# 1. Save conversation
conversation_data = {
    "title": "Sales Call with Mike",
    "duration_seconds": 300,
    "conversation_history": conversation_history,  # From your app
    "transcript": transcript_data,  # From your app
    "audio_duration": audio_duration
}

# Convert audio to base64 if you have audio data
audio_base64 = encode_audio_to_base64(audio_bytes) if audio_bytes else None

conv_result = db.save_conversation(user_id, conversation_data, audio_base64)

if conv_result["success"]:
    conversation_id = conv_result["conversation_id"]
    
    # 2. Save analysis
    analysis_result = db.save_analysis(user_id, conversation_id, analysis_data)
    
    if analysis_result["success"]:
        analysis_id = analysis_result["analysis_id"]
        
        # 3. Save best pitch
        best_pitch_result = db.save_best_pitch(user_id, conversation_id, analysis_id, best_pitch_data)
```

#### Update Your Flask Routes

Add these new routes to your `app.py`:

```python
from database_operations import DatabaseManager

db = DatabaseManager()

@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    """Save conversation to database"""
    try:
        # Get user from auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid auth token'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = db.get_current_user_id(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid user'}), 401
        
        data = request.json
        conversation_data = {
            "title": data.get("title", "Sales Conversation"),
            "duration_seconds": data.get("duration_seconds", 0),
            "conversation_history": data.get("conversation_history", []),
            "transcript": data.get("transcript", []),
            "audio_duration": data.get("audio_duration", 0),
            "user_agent": request.headers.get("User-Agent"),
            "ip_address": request.remote_addr
        }
        
        audio_data = data.get("audio_data")  # Base64 encoded
        
        result = db.save_conversation(user_id, conversation_data, audio_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    """Save analysis to database"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid auth token'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = db.get_current_user_id(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid user'}), 401
        
        data = request.json
        conversation_id = data.get("conversation_id")
        analysis_data = data.get("analysis_data")
        
        if not conversation_id or not analysis_data:
            return jsonify({"error": "Missing conversation_id or analysis_data"}), 400
        
        result = db.save_analysis(user_id, conversation_id, analysis_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_best_pitch', methods=['POST'])
def save_best_pitch():
    """Save best pitch to database"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid auth token'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = db.get_current_user_id(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid user'}), 401
        
        data = request.json
        conversation_id = data.get("conversation_id")
        analysis_id = data.get("analysis_id")
        best_pitch_data = data.get("best_pitch_data")
        
        if not all([conversation_id, analysis_id, best_pitch_data]):
            return jsonify({"error": "Missing required fields"}), 400
        
        result = db.save_best_pitch(user_id, conversation_id, analysis_id, best_pitch_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conversations', methods=['GET'])
def get_user_conversations():
    """Get all conversations for the current user"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid auth token'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = db.get_current_user_id(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid user'}), 401
        
        conversations = db.get_user_conversations(user_id)
        return jsonify({"conversations": conversations})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation_details(conversation_id):
    """Get complete conversation data including analysis and best pitch"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid auth token'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = db.get_current_user_id(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid user'}), 401
        
        data = db.get_complete_conversation_data(conversation_id, user_id)
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "Conversation not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### 4. Frontend Integration

Update your frontend to call these new endpoints:

```javascript
// Save conversation
async function saveConversation(conversationData) {
    const response = await fetch('/save_conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(conversationData)
    });
    return response.json();
}

// Save analysis
async function saveAnalysis(conversationId, analysisData) {
    const response = await fetch('/save_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            conversation_id: conversationId,
            analysis_data: analysisData
        })
    });
    return response.json();
}

// Save best pitch
async function saveBestPitch(conversationId, analysisId, bestPitchData) {
    const response = await fetch('/save_best_pitch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            conversation_id: conversationId,
            analysis_id: analysisId,
            best_pitch_data: bestPitchData
        })
    });
    return response.json();
}

// Get user conversations
async function getUserConversations() {
    const response = await fetch('/conversations', {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });
    return response.json();
}
```

### 5. Security Features

The database includes:
- **Row Level Security (RLS)**: Users can only access their own data
- **Foreign Key Constraints**: Ensures data integrity
- **Automatic Timestamps**: Tracks creation and update times
- **UUID Primary Keys**: Secure and unique identifiers

### 6. Performance Optimizations

- **Indexes**: Created on frequently queried columns
- **JSONB**: Efficient storage for complex data structures
- **Summary View**: Pre-joined data for common queries

### 7. Data Flow Example

1. User starts a conversation → Save to `conversations` table
2. User completes conversation → Update conversation with final data
3. Analysis is generated → Save to `analysis` table with `conversation_id`
4. Best pitch is generated → Save to `best_pitch` table with both `conversation_id` and `analysis_id`
5. User views history → Query `conversation_summary` view

This setup provides a complete, secure, and scalable database solution for your voice web chat application! 