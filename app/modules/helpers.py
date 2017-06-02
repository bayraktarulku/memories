import math


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    radius = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(long2 - long1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda) ** 2)

    c = 2 * math.atan2(a ** 0.5, (1-a) ** 0.5)
    return c * radius

if __name__ == '__main__':
    lat1, long1 = (40.988062, 29.065596)
    lat2, long2 = (40.987370, 29.066403)

    d = distance_on_unit_sphere(lat1, long1, lat2, long2)
    print(d)
