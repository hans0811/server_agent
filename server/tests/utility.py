import json


def load_json(file):
    try:
        with open(file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Cannot find the file")
        return None
