from geo_tools import verify_plane, verify_callsign
from aux_tools import download_file
from datetime import datetime


# removes extraneous characters from the hex code and makes it lowercase
def clean_hex_codes(plane_list: list) -> list:
    clean_list = list()
    for plane in plane_list:
        plane["hex"] = plane["hex"].replace("~", "").lower()
        clean_list.append(plane)
    return clean_list


# download data from airplanes.live and filter it (using spatial criteria)
def generate_filtered_list() -> list:
    unfiltered_planes = download_file()

    filtered_planes = [
        plane
        for plane in unfiltered_planes
        if (verify_plane(plane) and verify_callsign(plane))
    ]
    filtered_planes = clean_hex_codes(filtered_planes)
    return filtered_planes


# generates the part of a text message corresponding to a single plane
def generate_text(plane: dict) -> str:
    text = ""
    if "r" in plane:
        text += plane["r"]
        if "t" in plane:
            text += " " + plane["t"]
        if "flight" in plane:
            text += " " + plane["flight"]
        if "ownOp" in plane:
            text += " (" + plane["ownOp"] + ")"
    elif "hex" in plane:
        text += "ICAO: " + plane["hex"]

    return text


# Generates a text message from a list of planes
def generate_text_message(list_of_planes: list) -> str:
    output = ""
    for plane in list_of_planes:
        output += generate_text(plane) + "\n"
    return output


# Updates the dictionary containing planes for which messages have already been sent and
# the list containing aircraft which will be included in the text message
def remove_sent(plane_list: list, planes_to_ignore: dict) -> tuple[list, dict]:
    current_time = datetime.utcnow()

    # First, delete planes with old timestamps (>30 minutes)
    for hex_cod in list(planes_to_ignore.keys()):
        if (current_time - planes_to_ignore[hex_cod]).total_seconds() > 1800:
            del planes_to_ignore[hex_cod]

    # Remove already seen planes from the list that generates text messages
    plane_list[:] = [
        plane for plane in plane_list if (plane["hex"] not in planes_to_ignore.keys())
    ]

    # Add new planes to the ignore list
    for plane in plane_list:
        planes_to_ignore[plane["hex"]] = current_time

    return plane_list, planes_to_ignore
