import logging, copy, math
from timing import log_timing_, log_timing
from subsets import Subset
from segmentation import Segmentation
from points import Point
from vectors import Vector
from scipy.spatial import cKDTree
from utils import get_normal, get_angle, points_to_list


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@log_timing('computed normals',logger)
def compute_normals(subset):
    resultant_subset = copy.copy(subset)
    points = resultant_subset.points
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
    return resultant_subset

@log_timing('computed angles',logger)
def compute_angles(subset, reference_vector=[0,0,1]):
    resultant_subset = copy.copy(subset)
    points = resultant_subset.points
    for point in points:
        point.angle = math.degrees(float(get_angle(reference_vector, point.normal.to_xyz_list())))
    return resultant_subset

@log_timing('ran segmentation', logger)
def perform_segmentaion(subset, segmentation):
    resultant_subset = copy.copy(subset)
    resultant_subset.points = []
    points = subset.points
    for point in points:
        x = point.x
        y = point.y
        z = point.y
        if (x > self.segmentation.x_min
            and x < self.segmentation.x_max
            and y > self.segmentation.y_min
            and y < self.segmentation.y_max
            and z > self.segmentation.z_min
            and z < self.segmentation.z_max):
            resultant_subset.append(point)
    return resultant_subset

test_points = [
    Point(0,0,0,0,0,0,0),
    Point(1,1,0,0,0,0,0),
    Point(2,1,0,0,0,0,0),
    Point(1,2,0,0,0,0,0),
    Point(3,2,0,0,0,0,0),
    ]

#test_subset = Subset(points=test_points)
#test_subset_normals = compute_normals(test_subset)
#test_subset_angles = compute_angles(test_subset)

jameson_subset = Subset(path='data/Lidar/jameson.xyz', path_line_delim=' ')
jameson_subset_normal = compute_normals(jameson_subset)
jameson_subset_angles = compute_angles(jameson_subset_normal)

#a = compute_angles(n)
#jameson_segmentation = Segmentation(1,3,0,10,0,11)
#jameson_subset = Subset(superset_points, jameson_segmentation)
#jameson_subset.write_subset_points_to_file('data/jameson_subset.xyz')
