import json
import requests


# Definitions for dealing with the two JSON files
def write_chatid_json(data: list) -> None:
    with open("chatid_list.json", "w") as f:
        json.dump(data, f, indent=4)


def read_chatid_json() -> list:
    with open("chatid_list.json", "r") as f:
        return json.load(f)


def write_json(filename: str, data: list) -> None:
    acc_values(filename)
    with open(filename + ".json", "w") as f:
        json.dump(data, f, indent=4)


def read_json(filename: str) -> list:
    acc_values(filename)
    with open(filename + ".json", "r") as f:
        return json.load(f)


def acc_values(filename: str) -> None:
    values = ("chatid_list", "false_positive_callsigns", "prueba")
    if filename not in values:
        raise ValueError("Invalid JSON filename.")


# Download data from airplanes.live
def download_file() -> list:
    downloaded_file = requests.get("https://api.airplanes.live/v2/point/42.9/-2.75/80")
    return json.loads(downloaded_file.text)["ac"]
