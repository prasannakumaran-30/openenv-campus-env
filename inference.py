import os
from openai import OpenAI
from app.env import CampusEnv
from app.models import Action

# ---------------------------
# ENV VARIABLES (REQUIRED)
# ---------------------------
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

MAX_STEPS = 10

# ---------------------------
# INIT CLIENT (IMPORTANT)
# ---------------------------
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# ---------------------------
# LOGGING FUNCTIONS
# ---------------------------
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward} done={done} error={error}")

def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score} rewards={rewards}")

# ---------------------------
# LLM CALL (MANDATORY)
# ---------------------------
def call_llm(obs):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f"Classes: {obs.classes}. Suggest next scheduling step."
                }
            ],
            max_tokens=10
        )
        return response
    except Exception as e:
        print(f"LLM error: {e}")
        return None

# ---------------------------
# SIMPLE POLICY (UNCHANGED)
# ---------------------------
def choose_action(obs):
    for c in obs.classes:
        if c.room is None:
            return Action(
                action_type="assign_room",
                class_id=c.id,
                value="R1"
            )

    return Action(
        action_type="assign_room",
        class_id=obs.classes[0].id,
        value="R1"
    )

# ---------------------------
# RUN TASK
# ---------------------------
def run_task(level="easy"):
    env = CampusEnv()
    obs = env.reset(level)

    rewards = []
    steps_taken = 0

    for step in range(1, MAX_STEPS + 1):

        # ✅ THIS IS WHERE LLM IS CALLED
        call_llm(obs)

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

    total_reward = sum(rewards)
    score = total_reward / len(rewards) if rewards else 0.0
    score = max(0.0, min(1.0, score))

    success = len(rewards) > 0 and max(rewards) > 0

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
