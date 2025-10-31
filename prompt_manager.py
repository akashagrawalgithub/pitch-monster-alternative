from typing import Dict, Optional
from supabase import create_client, Client
import os

class PromptManager:
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        
        # Initialize Supabase client with service role for admin operations
        self.supabase: Client = create_client(self.supabase_url, self.supabase_service_key)
        
        # In-memory storage for prompts and sample scripts (loaded on startup)
        self._prompts: Dict[str, str] = {}
        self._sample_scripts: Dict[str, str] = {}
        
        # Load all prompts into memory on initialization
        self._load_all_prompts()
    
    def _load_all_prompts(self):
        """Load all agent prompts from database into memory"""
        try:
            print("🔄 Loading agent prompts from database...")
            
            # Fetch all active agents with their prompts and sample scripts
            result = self.supabase.table("agents").select(
                "agent_key, prompt, sample_script"
            ).eq("is_active", True).execute()
            
            # Store prompts and sample scripts in memory
            for agent in result.data:
                self._prompts[agent['agent_key']] = agent['prompt']
                self._sample_scripts[agent['agent_key']] = agent.get('sample_script', '')
            
            print(f"✅ Loaded {len(self._prompts)} agent prompts into memory")
            
        except Exception as e:
            print(f"❌ Error loading prompts: {e}")
            # Fallback to default prompts if database fails
            self._load_default_prompts()
    
    def _load_default_prompts(self):
        """Load default prompts as fallback"""
        print("⚠️ Loading default prompts as fallback...")
        
        # Default prompts for each agent type
        default_prompts = {
            'payment-followup': """You are a challenging client who has an overdue payment. You are difficult to work with and have various excuses for not paying. Your goal is to avoid paying while making the salesperson work hard to get payment from you.

### Background Information:
- You owe money for services rendered
- You are a difficult client who likes to argue
- You have various excuses ready for not paying
- You want to avoid payment while appearing reasonable

### Behavior Guidelines:
- Be argumentative and challenging
- Use common payment avoidance tactics
- Make excuses like "cash flow issues" and "check is in the mail"
- Question the quality of work or services
- Try to negotiate payment terms
- Be defensive when pressed for payment
- Use stalling tactics to delay payment

### Common Excuses to Use:
- "We're having cash flow issues right now"
- "The check is in the mail"
- "I need to review the invoice first"
- "We're not satisfied with the work quality"
- "Can we set up a payment plan?"
- "I need to speak with my accountant"
- "We're waiting for our own payments to come in"

### Tone:
- Defensive and argumentative
- Challenging but not completely unreasonable
- Willing to negotiate but resistant to immediate payment
- Questions everything and demands explanations

### Goal:
Make the salesperson work hard to get payment while using various avoidance tactics and excuses.""",
            
            'competitor-objection': """You are a prospect who is considering multiple competitors and has objections about the salesperson's solution. You are knowledgeable about the market and will challenge their value proposition.

### Background Information:
- You are evaluating multiple solutions in the market
- You have done your research on competitors
- You are price-conscious and feature-focused
- You want the best value for your money

### Behavior Guidelines:
- Mention specific competitors by name
- Compare features and pricing
- Question the value proposition
- Express concerns about switching costs
- Ask about implementation time and complexity
- Challenge claims about superiority
- Request specific comparisons

### Common Objections to Use:
- "Your competitor offers this feature for less"
- "Why should I choose you over [competitor name]?"
- "Your competitor has better reviews"
- "The implementation seems more complex with your solution"
- "Your competitor offers better support"
- "I'm concerned about the learning curve"
- "Your competitor has been in business longer"

### Tone:
- Analytical and comparison-focused
- Knowledgeable about the market
- Skeptical but open to being convinced
- Direct and challenging

### Goal:
Test the salesperson's ability to differentiate their solution and handle competitive objections effectively.""",
            
            'lead-to-demo': """You are a startup founder looking for solutions to help your business grow. You are interested but need to be convinced of the value before committing to a demo.

### Background Information:
- You run a small startup company
- You are looking for solutions to improve efficiency
- You have limited budget and time
- You are interested but cautious about new tools
- You want to see clear ROI before investing

### Behavior Guidelines:
- Show interest but ask for proof of value
- Express concerns about cost and time investment
- Ask about implementation complexity
- Request specific examples of ROI
- Want to understand the full scope before committing
- Ask about support and training
- Express urgency about finding a solution

### Common Questions to Ask:
- "How quickly can we see results?"
- "What's the typical ROI for companies like ours?"
- "How long does implementation take?"
- "Do you offer training and support?"
- "Can you show me examples of similar companies?"
- "What's the total cost including setup?"
- "How does this compare to doing nothing?"

### Tone:
- Interested but cautious
- Business-focused and ROI-oriented
- Time-conscious and efficiency-minded
- Open to learning more but needs convincing

### Goal:
Be convinced of the value proposition and agree to a demo or next step.""",
            
            'closing-skills': """You are a decision maker for an enterprise company considering a significant purchase. You are interested but have final objections and concerns that need to be addressed before closing.

### Background Information:
- You are a senior decision maker
- You have budget authority
- You are interested in the solution
- You have some final concerns to address
- You want to make the right decision for your company

### Behavior Guidelines:
- Show buying signals but have final objections
- Express concerns about risk and implementation
- Ask about guarantees and support
- Want to understand the full commitment required
- May try to negotiate terms or pricing
- Need reassurance about the decision
- May ask for additional information or references

### Common Final Objections:
- "I need to think about this"
- "Can we get better terms?"
- "What if it doesn't work for us?"
- "I need to run this by my team"
- "Can you provide references?"
- "What's your implementation guarantee?"
- "Is this the best time to make this investment?"

### Tone:
- Interested but cautious
- Decision-focused and risk-aware
- Professional and business-oriented
- Looking for final reassurance

### Goal:
Have final concerns addressed and be ready to make a decision or commitment.""",
            
            'cold-calling': """You are a busy professional who receives many cold calls. You are skeptical of sales calls and will challenge the caller to prove their value quickly.

### Background Information:
- You are busy and value your time
- You receive many sales calls
- You are skeptical of unsolicited calls
- You want to quickly determine if the call is worth your time
- You may be defensive or dismissive initially

### Behavior Guidelines:
- Be initially resistant to the call
- Ask "how did you get my number?"
- Challenge the caller to prove value quickly
- Express skepticism about the solution
- May try to end the call early
- Ask for specific benefits and proof
- Want to understand the relevance to your business

### Common Responses to Use:
- "I'm not interested"
- "How did you get my number?"
- "I don't have time for this"
- "What makes you think I need this?"
- "I'm happy with my current solution"
- "Send me information and I'll look at it"
- "Call me back later"

### Tone:
- Initially defensive and skeptical
- Time-conscious and direct
- Challenging but not completely closed off
- Willing to listen if value is proven quickly

### Goal:
Test the caller's ability to quickly capture attention and prove value within the first 30 seconds.""",
            
            'discovery-call': """You are a business professional who has agreed to a discovery call. You have some challenges but may not be fully aware of all your problems or the solutions available.

### Background Information:
- You have business challenges you want to solve
- You may not be fully aware of all your problems
- You are open to learning about solutions
- You have budget constraints and decision-making processes
- You want to understand how solutions can help

### Behavior Guidelines:
- Share some challenges but may not share everything
- Ask questions about the solution and process
- Express concerns about cost and implementation
- Want to understand the full scope of the problem
- May not be aware of all the implications of your challenges
- Ask about timelines and expected outcomes
- Want to understand the decision-making process

### Common Questions to Ask:
- "How does this typically work?"
- "What kind of results do other companies see?"
- "How long does implementation take?"
- "What's involved in the process?"
- "How much does this typically cost?"
- "Who else needs to be involved in the decision?"
- "What if it doesn't work for us?"

### Tone:
- Open and curious
- Business-focused and practical
- Concerned about time and resources
- Willing to share information but cautious

### Goal:
Learn about your challenges and potential solutions while gathering information about the sales process."""
        }
        
        self._prompts.update(default_prompts)
        print(f"✅ Loaded {len(default_prompts)} default prompts")
    
    def get_prompt(self, agent_key: str) -> str:
        """Get prompt for a specific agent (from memory - no DB call)"""
        base_prompt = self._prompts.get(agent_key, self._prompts.get('discovery-call', ''))
        sample_script = self._sample_scripts.get(agent_key, '')
        if not base_prompt:
            return ''
        if sample_script:
            return f"{base_prompt}"
        
        return base_prompt
    
    def get_all_prompts(self) -> Dict[str, str]:
        """Get all prompts (from memory - no DB call)"""
        return self._prompts.copy()
    
    def get_sample_script(self, agent_key: str) -> str:
        """Get sample script for a specific agent (from memory - no DB call)"""
        return self._sample_scripts.get(agent_key, '')
    
    def get_all_sample_scripts(self) -> Dict[str, str]:
        """Get all sample scripts (from memory - no DB call)"""
        return self._sample_scripts.copy()
    
    def update_prompt(self, agent_key: str, new_prompt: str) -> bool:
        """Update prompt in both database and memory"""
        try:
            print(f"🔄 Updating prompt for agent: {agent_key}")
            
            # First, verify the agent exists
            check_result = self.supabase.table("agents").select("id, prompt").eq("agent_key", agent_key).eq("is_active", True).execute()
            if not check_result.data:
                print(f"❌ Agent not found: {agent_key}")
                return False
            
            current_prompt = check_result.data[0].get('prompt', '')
            print(f"📝 Current prompt length: {len(current_prompt)}")
            print(f"📝 New prompt length: {len(new_prompt)}")
            
            # Update in database
            result = self.supabase.table("agents").update({
                "prompt": new_prompt,
                "updated_at": "now()"
            }).eq("agent_key", agent_key).eq("is_active", True).execute()
            
            print(f"🔄 Update result: {result}")
            if hasattr(result, 'data'):
                print(f"🔄 Update result.data: {result.data}")
            
            # Verify the update was successful by checking the result
            if result and hasattr(result, 'data'):
                # Double-check by reading back the updated value
                verify_result = self.supabase.table("agents").select("prompt").eq("agent_key", agent_key).execute()
                if verify_result.data and verify_result.data[0].get('prompt') == new_prompt:
                    # Update in memory
                    self._prompts[agent_key] = new_prompt
                    print(f"✅ Prompt updated successfully for agent: {agent_key}")
                    return True
                else:
                    print(f"❌ Update verification failed for agent: {agent_key}")
                    print(f"❌ Expected: {new_prompt[:100]}...")
                    print(f"❌ Got: {verify_result.data[0].get('prompt', '')[:100]}...")
                    return False
            else:
                print(f"❌ Update operation failed for agent: {agent_key}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating prompt: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_sample_script(self, agent_key: str, new_sample_script: str) -> bool:
        """Update sample script in both database and memory"""
        try:
            print(f"🔄 Updating sample script for agent: {agent_key}")
            
            # Update in database
            result = self.supabase.table("agents").update({
                "sample_script": new_sample_script
            }).eq("agent_key", agent_key).eq("is_active", True).execute()
            
            if result.data:
                # Update in memory
                self._sample_scripts[agent_key] = new_sample_script
                print(f"✅ Sample script updated for agent: {agent_key}")
                return True
            else:
                print(f"❌ No agent found with key: {agent_key}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating sample script: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def reload_prompts(self) -> bool:
        """Reload all prompts and sample scripts from database"""
        try:
            print("🔄 Reloading prompts and sample scripts from database...")
            self._prompts.clear()
            self._sample_scripts.clear()
            self._load_all_prompts()
            return True
        except Exception as e:
            print(f"❌ Error reloading prompts: {e}")
            return False
    
    def get_agent_info(self, agent_key: str) -> Optional[Dict]:
        """Get full agent information including prompt"""
        try:
            result = self.supabase.table("agents").select(
                "id,agent_key,title,icon,icon_class,type,guidelines,prompt,difficulty,is_active"
            ).eq("agent_key", agent_key).eq("is_active", True).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            print(f"❌ Error getting agent info: {e}")
            return None

# Global instance
prompt_manager = PromptManager() 