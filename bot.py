from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

DATA_FILE = "plant.json"

# Load plant data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    return {
        "health": 50,
        "happy": 0,
        "excited": 0,
        "stressed": 0,
        "tired": 0
    }

# Save plant data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Show plant stage
def plant_stage(health):
    if health < 20:
        return "🥀 Wilted Plant"
    elif health < 40:
        return "🌱 Seedling"
    elif health < 60:
        return "🌿 Sprout"
    elif health < 80:
        return "🌳 Young Tree"
    else:
        return "🌸 Blooming Tree"

@app.message("happy")
def happy(message, say):
    data = load_data()
    data["happy"] += 1
    data["health"] = min(100, data["health"] + 5)
    save_data(data)

    say(
        f"😊 Thanks for checking in!\n"
        f"Plant Health: {data['health']}%\n"
        f"{plant_stage(data['health'])}"
    )

@app.message("excited")
def excited(message, say):
    data = load_data()
    data["excited"] += 1
    data["health"] = min(100, data["health"] + 7)
    save_data(data)

    say(
        f"🎉 Excitement detected!\n"
        f"Plant Health: {data['health']}%\n"
        f"{plant_stage(data['health'])}"
    )

@app.message("stressed")
def stressed(message, say):
    data = load_data()
    data["stressed"] += 1
    data["health"] = max(0, data["health"] - 5)
    save_data(data)

    say(
        f"💙 Thanks for sharing.\n"
        f"Plant Health: {data['health']}%\n"
        f"{plant_stage(data['health'])}"
    )

@app.message("tired")
def tired(message, say):
    data = load_data()
    data["tired"] += 1
    data["health"] = max(0, data["health"] - 3)
    save_data(data)

    say(
        f"😴 Rest is important.\n"
        f"Plant Health: {data['health']}%\n"
        f"{plant_stage(data['health'])}"
    )

@app.message("garden")
def garden(message, say):
    data = load_data()

    say(
        f"""
🌱 *MoodSprout Garden*

Health: {data['health']}%
Stage: {plant_stage(data['health'])}

😊 Happy: {data['happy']}
🎉 Excited: {data['excited']}
😔 Stressed: {data['stressed']}
😴 Tired: {data['tired']}
"""
    )

@app.message("help")
def help_command(message, say):
    say(
        """
🌱 MoodSprout Commands

Type:
happy
excited
stressed
tired

View plant:
garden
"""
    )

if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    ).start()
