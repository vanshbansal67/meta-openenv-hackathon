import sys
import os
# Root directory ko path mein add karne ke liye
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ab tumhare purane imports kaam karenge
import os
from dotenv import load_dotenv
from openai import OpenAI
from envs.simulator import EmailTriageEnv

load_dotenv() # .env file se API key load karne ke liye
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_baseline():
    env = EmailTriageEnv()
    obs = env.reset()
    done = False
    total_reward = 0

    print("--- Starting Baseline Test ---")

    while not done:
        # Agent ko context dena (Prompt)
        prompt = f"""
        You are an email manager. Categorize this email.
        Sender: {obs.sender}
        Subject: {obs.subject}
        Body: {obs.body}

        Return your answer in JSON format matching the schema:
        {{ "priority": "High/Medium/Low", "category": "Support/Billing/Spam", "action_taken": "string" }}
        """

        # LLM se action lena
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Ya jo bhi tum use karna chaho
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        # Action parsing (Simplified)
        import json
        action_data = json.loads(response.choices[0].message.content)
        
        # Environment mein step lena
        from envs.models import EmailAction
        action = EmailAction(**action_data)
        
        step_resp = env.step(action)
        obs = step_resp.observation
        reward = step_resp.reward
        done = step_resp.done
        
        total_reward += reward
        print(f"Step Reward: {reward} | Total: {total_reward}")

    print(f"--- Final Score: {total_reward} ---")

if __name__ == "__main__":
    run_baseline()