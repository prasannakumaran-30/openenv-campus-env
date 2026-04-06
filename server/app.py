from fastapi import FastAPI
from app.env import CampusEnv
from app.models import Action

app = FastAPI()

env = CampusEnv()

# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/")
def root():
    return {"message": "OpenEnv Campus Running"}

# ---------------------------
# RESET ENDPOINT
# ---------------------------
@app.post("/reset")
def reset():
    obs = env.reset("easy")

    return {
        "observation": obs.__dict__,
        "info": {}
    }

# ---------------------------
# STEP ENDPOINT
# ---------------------------
@app.post("/step")
def step(action: dict):
    act = Action(**action)

    result = env.step(act)

    return {
        "observation": result["observation"].__dict__,
        "reward": result["reward"],
        "done": result["done"],
        "info": result.get("info", {})
    }
