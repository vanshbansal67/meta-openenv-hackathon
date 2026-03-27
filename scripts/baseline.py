import sys
import os
import json
import time
import io
from dotenv import load_dotenv
from openai import OpenAI

# Force UTF-8 encoding for standard output (Windows Console fix for emojis)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Root directory ko path mein add karna (for imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Envs se models aur simulator load karna
try:
    from envs.simulator import EmailTriageEnv
    from envs.models import EmailAction
except ImportError:
    print("Error: 'envs' folder nahi mila. Make sure aap project root se run kar rahe hain.")
    sys.exit(1)

# .env se key load karna
load_dotenv()

# OpenAI Client Setup (Gemini Compatible)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_baseline():
    env = EmailTriageEnv()
    obs = env.reset()
    done = False
    total_reward = 0

    print("🚀 --- Starting Meta OpenEnv Baseline Test ---")

    while not done:
        # 1. Prompt Taiyar karna (JSON instruction ke saath)
        prompt = f"""
        Analyze and categorize this email.
        Sender: {obs.sender}
        Subject: {obs.subject}
        Body: {obs.body}

        Return your answer ONLY in JSON format with these keys:
        {{ "priority": "High/Medium/Low", "category": "Support/Billing/Spam", "action_taken": "short string" }}
        """

        try:
            # 2. LLM Call (Gemini 2.5 Flash)
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,           # Token limit increased to prevent cutoff
                temperature=0.2,          # Kam temperature = Zyada accurate JSON
            )

            # 3. Response Parsing
            content = response.choices[0].message.content
            print(f"DEBUG RAW CONTENT -> {content}")

            # Safe json parsing
            import re
            match = re.search(r'\{.*\}', content, flags=re.DOTALL)
            if match:
                content = match.group(0)

            action_data = json.loads(content)
            
            # Print for debugging
            print(f"DEBUG: Agent Response -> {action_data}")

            # 4. Environment mein Step lena
            action = EmailAction(**action_data)
            
            # Note: OpenEnv ke version ke hisab se return values check karna
            # Agar 'step' 3 values return kare:
            obs = env.step(action) 
            
            reward = getattr(obs, 'reward', 0)
            done = getattr(obs, 'done', False)
            
            total_reward += reward
            print(f"✅ Step Reward: {reward} | Total: {total_reward}")

            # 5. Rate Limit se bachne ke liye chota sa pause (Free Tier ke liye)
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            break

    print(f"\n🏆 --- Final Score: {total_reward} ---")

if __name__ == "__main__":
    run_baseline()