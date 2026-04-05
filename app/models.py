from pydantic import BaseModel
from typing import List, Optional

class Class(BaseModel):
    id: int
    time: str
    faculty: str
    room: Optional[str] = None
    priority: int = 1

class Observation(BaseModel):
    classes: List[Class]
    step_count: int
    last_action: Optional[str]

class Action(BaseModel):
    action_type: str  # assign_room, reschedule, cancel
    class_id: int
    value: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str