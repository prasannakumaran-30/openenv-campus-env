from app.env import CampusEnv
from app.models import Action

env = CampusEnv()

obs = env.reset()
print("RESET OUTPUT:")
print(obs)

for i in range(5):
    print(f"\n--- STEP {i+1} ---")
    result = env.step(Action(action_type="assign_room", class_id=1, value="R1"))
    print(result)