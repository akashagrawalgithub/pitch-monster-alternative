-- Create agents table for storing AI training personas
CREATE TABLE agents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    agent_key VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    icon VARCHAR(10) NOT NULL,
    icon_class VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    guidelines TEXT NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'medium',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_agents_agent_key ON agents(agent_key);
CREATE INDEX idx_agents_is_active ON agents(is_active);
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_difficulty ON agents(difficulty);

-- Apply updated_at trigger to agents table
CREATE TRIGGER update_agents_updated_at 
    BEFORE UPDATE ON agents 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for agents (read-only for all authenticated users)
CREATE POLICY "All authenticated users can view agents" ON agents
    FOR SELECT USING (auth.role() = 'authenticated');

-- Grant necessary permissions
GRANT SELECT ON agents TO authenticated;

-- Insert the agent data from the static file
INSERT INTO agents (agent_key, title, icon, icon_class, type, guidelines, difficulty) VALUES
(
    'payment-followup',
    'Payment Follow-up - Challenging Client',
    '💰',
    'icon-payment',
    'Payment Collection',
    'Practice handling overdue payment conversations with challenging clients who have various excuses and objections. Learn to maintain professionalism while being firm about payment terms, handle common objections like "cash flow issues" and "check is in the mail," and develop strategies for escalating when necessary.',
    'medium'
),
(
    'competitor-objection',
    'Competitor Objection - Market Competition',
    '💬',
    'icon-competitor',
    'Objection Handling',
    'Handle objections when prospects mention competitors. Learn to differentiate your solution and highlight unique value propositions. Practice techniques for addressing price comparisons, feature comparisons, and building confidence in your solution over alternatives.',
    'hard'
),
(
    'lead-to-demo',
    'Lead to Demo - Exporter Startup Company',
    '👥',
    'icon-lead',
    'Lead Qualification',
    'Convert interested leads into demo bookings through effective questioning and value proposition delivery. Practice discovery techniques to understand prospect needs, budget, authority, and timeline. Learn to create urgency and demonstrate clear value to secure demo commitments.',
    'easy'
),
(
    'closing-skills',
    'Closing Skills - Enterprise Deal',
    '🤝',
    'icon-closing',
    'Deal Closing',
    'Master the art of closing deals with various closing techniques and handling last-minute objections. Practice assumptive closes, trial closes, and alternative choice closes. Learn to identify buying signals and overcome final objections to secure commitments.',
    'hard'
),
(
    'cold-calling',
    'Cold Calling - B2B Prospecting',
    '📞',
    'icon-cold-calling',
    'Prospecting',
    'Perfect your cold calling techniques, break through gatekeepers, and capture prospect attention quickly. Practice opening statements, handling initial resistance, and creating interest in your solution within the first 30 seconds of the call.',
    'medium'
),
(
    'discovery-call',
    'Discovery Call - Solution Selling',
    '🔍',
    'icon-discovery',
    'Needs Analysis',
    'Learn effective questioning techniques to uncover pain points, budget, and decision-making processes. Practice SPIN selling methodology, develop consultative selling skills, and learn to build trust while gathering critical information for solution development.',
    'medium'
); 