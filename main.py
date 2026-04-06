from fastapi import FastAPI
from app.env import CampusEnv
from app.models import Action

app = FastAPI()
@app.get("/")
def root():
    return {"message": "OpenEnv Campus Running"}

env = CampusEnv()

@app.post("/reset")
def reset():
    obs = env.reset("easy")
    return {"observation": obs}

@app.post("/step")
def step(action: dict):
    act = Action(**action)
    result = env.step(act)
    return result

@app.get("/state")
def state():
    return {"state": env.state()}
