from pydantic import Field
from openenv.core import Action, Observation
from typing import List, Optional

# Agent kya DEKHEGA (Observation)
class EmailObservation(Observation):
    sender: str = Field(description="Email bhejne wale ka naam")
    subject: str = Field(description="Email ka subject line")
    body: str = Field(description="Email ka poora content")
    current_queue_size: int = Field(description="Kitne emails pending hain")

# Agent kya KAREGA (Action)
class EmailAction(Action):
    priority: str = Field(description="Email ki priority: 'High', 'Medium', ya 'Low'")
    category: str = Field(description="Category: 'Support', 'Billing', ya 'Spam'")
    action_taken: str = Field(description="Brief note ki agent ne kya kiya")