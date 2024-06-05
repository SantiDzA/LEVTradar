from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from aux_tools import read_json


# We'll use this class to associate a maximum altitude to a polygon bounded by geographic coordinates
class Airspace:
    def __init__(self, max_altitude, coords):
        self.max_altitude = int(max_altitude)
        self.coords = Polygon(coords)


# Define the relevant sections of airspace
espaciovit = Airspace(
    10000,
    [
        (43.0628691, -3.0267348),
        (43.0267384, -2.3730482),
        (42.8950835, -2.1574416),
        (42.6814269, -1.970674),
        (42.4558887, -2.447206),
        (42.4335951, -2.9525784),
        (42.5409415, -3.3343533),
        (42.6965678, -3.4373481),
    ],
)

convex_polygons = (espaciovit,)

# Verify that a given plane is in one of the previously defined airspace sectors
def verify_plane(plane: dict) -> bool:
    point = Point(plane["lat"], plane["lon"])
    detected = False
    for convex_polygon in convex_polygons:
        is_contained_in_polygon = convex_polygon.coords.contains(point)
        if is_contained_in_polygon and plane["alt_baro"] == "ground":
            detected = True
            break
        elif (
            is_contained_in_polygon
            and int(plane["alt_baro"]) < convex_polygon.max_altitude
        ):
            detected = True
            break
    return detected


# Filter planes headed towards other airports based on their callsign
def verify_callsign(plane: dict) -> bool:
    false_positive_callsigns = read_json("false_positive_callsigns")
    if plane.get("flight", "").strip() in false_positive_callsigns:
        return False
    return True
