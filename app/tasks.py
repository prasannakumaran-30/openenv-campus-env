# ---------------------------
# TASK 1: EASY
# ---------------------------
def easy_task():
    from app.env import CampusEnv
    env = CampusEnv()
    return env.reset("easy")

def easy_grader(env):
    return sum(1 for c in env.classes if c.room is not None)


# ---------------------------
# TASK 2: MEDIUM
# ---------------------------
def medium_task():
    from app.env import CampusEnv
    env = CampusEnv()
    return env.reset("medium")

def medium_grader(env):
    return sum(1 for c in env.classes if c.room is not None)


# ---------------------------
# TASK 3: HARD
# ---------------------------
def hard_task():
    from app.env import CampusEnv
    env = CampusEnv()
    return env.reset("hard")

def hard_grader(env):
    return sum(1 for c in env.classes if c.room is not None)


# ---------------------------
# REQUIRED FUNCTION (DO NOT REMOVE)
# ---------------------------
def get_task(level):
    if level == "easy":
        return easy_task()
    elif level == "medium":
        return medium_task()
    elif level == "hard":
        return hard_task()
    else:
        raise ValueError(f"Unknown task level: {level}")
