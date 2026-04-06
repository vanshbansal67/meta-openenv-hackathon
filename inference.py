import sys
import os
import json
import time
import io
import re
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Force UTF-8 encoding for standard output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Root directory path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from envs.simulator import EmailTriageEnv
    from envs.models import EmailAction
except ImportError:
    # Using stderr so it doesn't break Meta's stdout parser
    sys.stderr.write("Error: 'envs' folder not found.\n")
    sys.exit(1)

load_dotenv()

# ==========================================
# META REQUIRED VARIABLES
# ==========================================
API_BASE_URL = os.getenv("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
# Meta prioritizes HF_TOKEN, fallback to OPENAI_API_KEY for local testing
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")

BENCHMARK_NAME = "email_triage_env"

# ==========================================
# STRICT LOGGING FUNCTIONS (DO NOT MODIFY)
# ==========================================
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

# ==========================================
# MAIN INFERENCE LOOP
# ==========================================
def run_inference():
    client = OpenAI(
        api_key=API_KEY,
        base_url=API_BASE_URL
    )
    
    tasks = ["easy", "medium", "hard"]

    for task_id in tasks:
        env = EmailTriageEnv(task_id=task_id)
        obs = env.reset()
        
        history = []
        rewards = []
        steps_taken = 0
        final_score = 0.0
        done = False
        
        # 1. Log Start
        log_start(task=task_id, env=BENCHMARK_NAME, model=MODEL_NAME)

        while not done:
            steps_taken += 1
            error_msg = None
            action_str = "{}"
            reward = 0.0
            
            prompt = f"""
            Analyze and categorize this email.
            Sender: {obs.sender}
            Subject: {obs.subject}
            Body: {obs.body}

            Return your answer ONLY in JSON format with these keys:
            {{ "priority": "High/Medium/Low", "category": "Support/Billing/Spam", "action_taken": "short string" }}
            """

            max_retries = 3
            action_data = None
            
            for attempt in range(max_retries):
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=200,
                        temperature=0.2,
                    )
                    content = response.choices[0].message.content
                    
                    match = re.search(r'\{.*\}', content, flags=re.DOTALL)
                    if match:
                        content = match.group(0)

                    action_data = json.loads(content)
                    action_str = json.dumps(action_data) # Compact string for logging
                    break 
                except Exception as e:
                    time.sleep(2)
            else:
                action_data = {"priority": "Low", "category": "Support", "action_taken": "Fallback due to error"}
                action_str = json.dumps(action_data)
                error_msg = "JSON Parse Failure"

            try:
                # Take step in environment
                action = EmailAction(**action_data)
                obs = env.step(action)
                
                # Support both object attributes and dict-like returns
                reward = getattr(obs, 'reward', 0.0)
                done = getattr(obs, 'done', False)
                metadata = getattr(obs, 'metadata', {})
                
            except Exception as e:
                done = True
                error_msg = str(e)
                metadata = {}

            rewards.append(reward)

            # 2. Log Step
            log_step(step=steps_taken, action=action_str, reward=reward, done=done, error=error_msg)

            if done:
                final_grader_score = metadata.get("grader_score", 0.0)
                final_score = float(final_grader_score)
                break

            time.sleep(3) # Rate limit protection

        # 3. Log End (Score is strictly between 0.0 and 1.0)
        final_score = max(0.0, min(1.0, final_score)) # Clamp safely
        success = final_score >= 0.5 # Define success threshold
        
        log_end(success=success, steps=steps_taken, score=final_score, rewards=rewards)

if __name__ == "__main__":
    run_inference()