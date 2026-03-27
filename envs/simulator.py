from openenv.core import Environment
from .models import EmailObservation, EmailAction

class EmailTriageEnv(Environment[EmailAction, EmailObservation, dict]):
    def __init__(self, task_id: str = "easy"):
        super().__init__()
        self.task_id = task_id
        # 3 Tasks with increasing difficulty
        self.all_tasks = {
            "easy": [
                {"sender": "boss@co.com", "subject": "Urgent", "body": "Finish report.", "p": "High", "c": "Support"},
                {"sender": "spam@ads.com", "subject": "Win Cash", "body": "Click here.", "p": "Low", "c": "Spam"}
            ],
            "medium": [
                {"sender": "hr@co.com", "subject": "Policy Update", "body": "Read new rules.", "p": "Medium", "c": "Support"},
                {"sender": "billing@aws.com", "subject": "Invoice", "body": "Payment failed.", "p": "High", "c": "Billing"}
            ],
            "hard": [
                {"sender": "client@dev.com", "subject": "Bug Report", "body": "System is down in production!", "p": "High", "c": "Support"},
                {"sender": "marketing@co.com", "subject": "Draft", "body": "Review the blog post.", "p": "Low", "c": "Support"}
            ]
        }
        self.reset()

    def reset(self) -> EmailObservation:
        self.current_emails = self.all_tasks.get(self.task_id, self.all_tasks["easy"])
        self.current_index = 0
        self.total_points = 0
        return self._get_obs()

    def _get_obs(self):
        email = self.current_emails[self.current_index]
        return EmailObservation(
            sender=email["sender"],
            subject=email["subject"],
            body=email["body"],
            current_queue_size=len(self.current_emails) - self.current_index
        )

    def step(self, action: EmailAction, timeout_s: float | None = None, **kwargs) -> EmailObservation:
        correct_data = self.current_emails[self.current_index]
        reward = 0.0
        
        # --- REWARD SHAPING (Winning Logic) ---
        # 1. Partial Reward for Category (0.3)
        if action.category == correct_data["c"]:
            reward += 0.3
        
        # 2. Points for Priority (0.7)
        if action.priority == correct_data["p"]:
            reward += 0.7
            
        self.total_points += reward
        self.current_index += 1
        done = self.current_index >= len(self.current_emails)
        
        # Grader Score Calculation (Must be 0.0 to 1.0)
        final_score = self.total_points / len(self.current_emails) if done else 0.0
        
        if not done:
            obs = self._get_obs()
        else:
            obs = EmailObservation(sender="", subject="", body="", current_queue_size=0)
            
        obs.reward = reward
        obs.done = done
        obs.metadata = {"grader_score": final_score}
        return obs

    @property
    def state(self) -> dict:
        return {"task": self.task_id, "index": self.current_index}