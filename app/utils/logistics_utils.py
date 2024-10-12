import math

def calculate_proximity(location1: str, location2: str) -> float:
    """
    Calculate the distance between two locations using the Haversine formula.
    
    :param location1: Coordinates of the first location ('latitude,longitude').
    :param location2: Coordinates of the second location ('latitude,longitude').
    :return: Distance in kilometers.
    """
    lat1, lon1 = map(float, location1.split(','))
    lat2, lon2 = map(float, location2.split(','))

    R = 6371.0  # Radius of the Earth in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
