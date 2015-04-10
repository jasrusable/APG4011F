import logging
from timing import log_timing, with_log_timing
from subsets import Subset
from points import Point, Vector
from segmentation import Segmentation
from scipy.spatial import cKDTree
import scipy.linalg as linalg


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def points_to_list(points):
    list_of_points = []
    for point in points:
        list_of_points.append([point.x, point.y, point.z])
    return list_of_points


@log_timing('getting points from file', logger)
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
    u, s, v = linalg.svd(points)
    return v[2]

@log_timing('compute normals',logger)
def compute_normals(points):
    kd_tree = cKDTree(points_to_list(points))
    for point in points:
        distances, indexs = kd_tree.query(point.to_xyz_list(), k=5)
        neighbors = []
        for index in indexs:
            neighbors.append([points[index].x, points[index].y, points[index].z])
        normal = get_normal(neighbors)
        point.normal = Vector(x=normal[0], y=normal[1], z=normal[2])
    return points


test_points = [
    Point(0,0,0,0,0,0,0,None),
    Point(1,1,0,0,0,0,0,None),
    Point(2,1,0,0,0,0,0,None),
    Point(1,2,0,0,0,0,0,None),
    Point(3,2,0,0,0,0,0,None),
    ]

superset_points = get_list_of_points_from_file('data/Lidar/jameson.xyz')
#jameson_segmentation = Segmentation(1,3,0,10,0,11)
#jameson_subset = Subset(superset_points, jameson_segmentation)
#jameson_subset.write_subset_points_to_file('data/jameson_subset.xyz')
