import os
from openai import OpenAI
from app.env import CampusEnv
from app.models import Action

# ---------------------------
# ENV VARIABLES (REQUIRED)
# ---------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline-model")
API_KEY = os.getenv("OPENAI_API_KEY", "")

MAX_STEPS = 10
MAX_TOTAL_REWARD = 10.0  # normalization

# ---------------------------
# LOGGING FUNCTIONS (STRICT)
# ---------------------------
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward} done={done} error={error}")

def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score} rewards={rewards}")

# ---------------------------
# SIMPLE BASELINE POLICY
# ---------------------------
def choose_action(obs):
    # pick first class without room
    for c in obs.classes:
        if c.room is None:
            return Action(
                action_type="assign_room",
                class_id=c.id,
                value="R1"
            )

    # fallback
    return Action(
        action_type="assign_room",
        class_id=obs.classes[0].id,
        value="R1"
    )

# ---------------------------
# RUN SINGLE TASK
# ---------------------------
def run_task(level="easy"):
    env = CampusEnv()
    obs = env.reset(level)

    rewards = []
    steps_taken = 0

    for step in range(1, MAX_STEPS + 1):
        action = choose_action(obs)

        result = env.step(action)

        obs = result["observation"]
        reward = result["reward"]
        done = result["done"]

        rewards.append(reward)
        steps_taken = step

        log_step(
            step=step,
            action=str(action),
            reward=reward,
            done=done,
            error=None
        )

        if done:
            break

    # ---------------------------
    # SCORE CALCULATION
    # ---------------------------
    total_reward = sum(rewards)
    score = total_reward / len(rewards) if rewards else 0.0
    score = max(0.0, min(1.0, score))  # clamp

    success = len(rewards) > 0 and max(rewards) > 0 # threshold

    log_end(
        success=success,
        steps=steps_taken,
        score=score,
        rewards=rewards
    )

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    log_start(task="easy", env="campus-env", model=MODEL_NAME)
    run_task("easy")
    time.sleep(5)
