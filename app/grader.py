from app.models import Reward

def has_clash(state):
    seen = set()
    for c in state:
        if c.room is None:
            continue
        key = (c.time, c.room)
        if key in seen:
            return True
        seen.add(key)
    return False


def grade(state, action):
    reward = 0.0

    # reward assigning room based on priority
    for c in state:
        if c.id == action.class_id and c.room is not None:
            reward += 0.1 * c.priority  # HIGH class → more reward

    # clash penalty (strong)
    if has_clash(state):
        reward -= 0.6

    # penalty for unassigned HIGH priority classes
    for c in state:
        if c.room is None:
            reward -= 0.05 * c.priority

    # clamp
    reward = max(0.0, min(1.0, reward))

    return Reward(value=reward, reason="priority_evaluated")