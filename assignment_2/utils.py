import logging, math
import scipy.linalg as linalg
from timing import log_timing



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))

def get_unit_length(v):
    return math.sqrt(dotproduct(v, v))

def get_angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (get_unit_length(v1) * get_unit_length(v2)))

def get_normal(points):
    temp = []
    for point in points:
        temp.append([point.x, point.y, point.z])
    u, s, v = linalg.svd(temp)
    return v[2]

@log_timing('converted Points to lists',logger)
def points_to_list(points):
    list_of_points = []
    for point in points:
        list_of_points.append([point.x, point.y, point.z])
    return list_of_points
