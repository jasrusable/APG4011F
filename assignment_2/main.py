import logging
import math
import scipy.linalg as linalg
from timing import log_timing_, log_timing
from subsets import Subset
from points import Point, Vector
from segmentation import Segmentation
from scipy.spatial import cKDTree


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@log_timing('converted Points to lists',logger)
def points_to_list(points):
    list_of_points = []
    for point in points:
        list_of_points.append([point.x, point.y, point.z])
    return list_of_points

@log_timing('read points from file', logger)
def get_list_of_points_from_file(path='superset.xyz', delim=' '):
    points = []
    with open(path, 'r') as f:
        for line in f:
            parts = line.split(delim)
            point = Point(
                x = float(parts[0]),
                y = float(parts[1]),
                z = float(parts[2]),
                intensity = float(parts[3]),
                red = float(parts[4]),
                green = float(parts[5]),
                blue = float(parts[6]),
                normal = None,
                )
            points.append(point)
    return points

def get_normal(points):
    temp = []
    for point in points:
        temp.append([point.x, point.y, point.z])
    u, s, v = linalg.svd(temp)
    return v[2]

@log_timing('computed normals',logger)
def compute_normals(points):
    with log_timing_('built tree', logger):
        kd_tree = cKDTree(points_to_list(points))
    with log_timing_('loop for computing normals', logger):
        for point in points:
            distances, indexs = kd_tree.query(point.to_xyz_list(), k=5)
            neighbors = []
            for index in indexs:
                neighbors.append(points[index])
            # get_normal is very slow
            normal = get_normal(neighbors)
            point.normal = Vector(x=normal[0], y=normal[1], z=normal[2])
    return points

@log_timing('computed angles',logger)
def compute_angles(points):
    vert_vec = [0,0,1]
    for point in points:
        point.angle = math.degrees(float(get_angle(vert_vec, point.normal.to_xyz_list())))
    return points

def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))

def get_unit_length(v):
    return math.sqrt(dotproduct(v, v))

def get_angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (get_unit_length(v1) * get_unit_length(v2)))

test_points = [
    Point(0,0,0,0,0,0,0),
    Point(1,1,0,0,0,0,0),
    Point(2,1,0,0,0,0,0),
    Point(1,2,0,0,0,0,0),
    Point(3,2,0,0,0,0,0),
    ]

superset_points = get_list_of_points_from_file('data/Lidar/jameson.xyz')
n = compute_normals(superset_points)
#a = compute_angles(n)
#jameson_segmentation = Segmentation(1,3,0,10,0,11)
#jameson_subset = Subset(superset_points, jameson_segmentation)
#jameson_subset.write_subset_points_to_file('data/jameson_subset.xyz')
