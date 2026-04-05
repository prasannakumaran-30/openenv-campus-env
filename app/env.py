from app.models import Observation, Action
from app.tasks import get_task
from app.grader import grade
import random


class CampusEnv:
    def __init__(self):
        self.state_data = []
        self.rooms = []
        self.steps = 0
        self.max_steps = 10

    # ---------------------------
    # RESET (supports task levels)
    # ---------------------------
    def reset(self, level="easy"):
        task = get_task(level)

        self.state_data = task["classes"]
        self.rooms = task["rooms"]
        self.steps = 0

        return Observation(
            classes=self.state_data,
            step_count=0,
            last_action=None
        )

    # ---------------------------
    # DISRUPTION LOGIC
    # ---------------------------
    def apply_disruption(self):
        event = random.choice([
            "none",
            "faculty_unavailable",
            "room_blocked",
            "new_class"
        ])

        if event == "faculty_unavailable" and self.state_data:
            c = random.choice(self.state_data)
            c.faculty = "UNAVAILABLE"

        elif event == "room_blocked" and self.rooms:
            blocked_room = random.choice(self.rooms)
            for c in self.state_data:
                if c.room == blocked_room:
                    c.room = None

        elif event == "new_class":
            if self.state_data:
                new_id = max(c.id for c in self.state_data) + 1
            else:
                new_id = 1

            self.state_data.append(
                type(self.state_data[0])(
                    id=new_id,
                    time="11AM",
                    faculty="NEW",
                    priority=1
                )
            )

    # ---------------------------
    # STEP FUNCTION
    # ---------------------------
    def step(self, action: Action):
        self.steps += 1

        # ---------------------------
        # APPLY ACTION
        # ---------------------------
        if action.action_type == "assign_room":
            for c in self.state_data:
                if c.id == action.class_id:
                    if action.value in self.rooms:
                        c.room = action.value

        elif action.action_type == "reschedule":
            for c in self.state_data:
                if c.id == action.class_id:
                    c.time = action.value

        elif action.action_type == "cancel":
            self.state_data = [
                c for c in self.state_data if c.id != action.class_id
            ]

        # ---------------------------
        # APPLY DISRUPTION
        # ---------------------------
        self.apply_disruption()

        # ---------------------------
        # CALCULATE REWARD
        # ---------------------------
        reward = grade(self.state_data, action)

        # ---------------------------
        # DONE CONDITION
        # ---------------------------
        done = (
            self.steps >= self.max_steps or
            all(c.room is not None for c in self.state_data)
        )

        return {
            "observation": Observation(
                classes=self.state_data,
                step_count=self.steps,
                last_action=str(action)
            ),
            "reward": reward.value,
            "done": done,
            "info": {}
        }

    # ---------------------------
    # CURRENT STATE
    # ---------------------------
    def state(self):
        return self.state_data