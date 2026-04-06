from fastapi import FastAPI
from app.env import CampusEnv
from app.models import Action
import uvicorn

app = FastAPI()
env = CampusEnv()

# ---------------------------
# ROOT
# ---------------------------
@app.get("/")
def root():
    return {"message": "OpenEnv Campus Running"}

# ---------------------------
# RESET
# ---------------------------
@app.post("/reset")
def reset():
    obs = env.reset("easy")

    return {
        "observation": obs.__dict__,
        "info": {}
    }

# ---------------------------
# STEP
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

# ---------------------------
# MAIN ENTRYPOINT (REQUIRED)
# ---------------------------
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    main()
