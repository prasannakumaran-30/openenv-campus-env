from app.models import Class

def get_task(level="easy"):
    
    if level == "easy":
        classes = [
            Class(id=1, time="9AM", faculty="A", priority=2),
            Class(id=2, time="10AM", faculty="B", priority=1),
        ]

    elif level == "medium":
        classes = [
            Class(id=1, time="9AM", faculty="A", priority=3),
            Class(id=2, time="9AM", faculty="B", priority=1),
            Class(id=3, time="10AM", faculty="C", priority=2),
        ]

    elif level == "hard":
        classes = [
            Class(id=1, time="9AM", faculty="A", priority=3),
            Class(id=2, time="9AM", faculty="B", priority=2),
            Class(id=3, time="9AM", faculty="C", priority=1),
            Class(id=4, time="10AM", faculty="D", priority=3),
        ]

    rooms = ["R1", "R2"]

    return {
        "classes": classes,
        "rooms": rooms
    }