import json
import os

STATE_FILE = "src/storage/data/states.json"


def load_states():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_states(states):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(states, file, indent=4)


def save_state(filename, data):
    states = load_states()
    states[filename] = data
    save_states(states)


def get_state(filename):
    states = load_states()
    return states.get(filename)


def delete_state(filename):
    states = load_states()
    if filename in states:
        del states[filename]
        save_states(states)